#!/usr/bin/env python3
import os, time, argparse, ctypes
from io import BytesIO
import numpy as np
from PIL import Image as PILImage

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from sensor_msgs.msg import CompressedImage, Image
from std_msgs.msg import String

# ---- Defaults (no env exports needed) ---------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL_NAME = "fastdepth_256x320_edgetpu.tflite"
DEFAULT_MODEL_PATH = os.path.join(SCRIPT_DIR, DEFAULT_MODEL_NAME)

DEFAULT_IN_TOPIC  = "/olive/camera/id001/image/compressed"
DEFAULT_OUT_BASE  = "/olive/camera/id001/depth_color"
DEFAULT_STATUS    = "/olive/camera/id001/tpu_status"
DEFAULT_EVERY_N   = 1           # run inference every frame
DEFAULT_JPEG_QLTY = 60          # good speed/size balance
DEFAULT_PUBLISH   = "compressed"  # choices: compressed, raw, both
DEFAULT_ROTATE    = 0           # 0/90/180/270 degrees
DEFAULT_RESAMPLE  = "nearest"   # nearest|bilinear for preprocess/resize

# Try lightweight TFLite first; fall back to TF's tflite if present
Interpreter = None
load_delegate = None
try:
    from tflite_runtime.interpreter import Interpreter as _I, load_delegate as _LD
    Interpreter, load_delegate = _I, _LD
except Exception:
    try:
        from tensorflow.lite import Interpreter as _I  # CPU-only if no delegate
        Interpreter, load_delegate = _I, (lambda *_a, **_k: None)
    except Exception:
        Interpreter = None

def jet_colormap(depth: np.ndarray) -> np.ndarray:
    """Approximate JET colormap for values normalized to [0,1]. Returns uint8 RGB."""
    d = np.clip(depth, 0.0, 1.0)
    r = np.clip(1.5 - np.abs(4*d - 3), 0, 1)
    g = np.clip(1.5 - np.abs(4*d - 2), 0, 1)
    b = np.clip(1.5 - np.abs(4*d - 1), 0, 1)
    rgb = np.stack([r, g, b], axis=-1) * 255.0
    return rgb.astype(np.uint8)

class MonoDepthTPU(Node):
    def __init__(self, args):
        super().__init__('olive_tpu_depth')

        qos = QoSProfile(depth=5)
        qos.reliability = ReliabilityPolicy.BEST_EFFORT
        qos.durability  = DurabilityPolicy.VOLATILE

        self.in_topic    = args.in_topic
        self.out_base    = args.out_base            # raw rgb8 base
        self.out_comp    = self.out_base + '/compressed'
        self.status_topic = args.status_topic
        self.model_path  = args.model
        self.every_n     = max(1, args.every_n)
        self.jpeg_quality = int(args.jpeg_quality)
        self.publish_mode = args.publish
        self.rotate_deg   = int(args.rotate)
        self.resample     = PILImage.NEAREST if args.resample == "nearest" else PILImage.BILINEAR

        # Publishers
        if self.publish_mode in ("raw", "both"):
            self.pub_raw  = self.create_publisher(Image, self.out_base, qos)
        else:
            self.pub_raw  = None
        if self.publish_mode in ("compressed", "both"):
            self.pub_comp = self.create_publisher(CompressedImage, self.out_comp, qos)
        else:
            self.pub_comp = None
        self.pub_status = self.create_publisher(String, self.status_topic, 10)

        # Model / delegate
        self.interpreter = None
        self.use_tpu = False
        self.input_h = self.input_w = None
        self.input_dtype = None
        self.frame_count = 0

        self._init_model()

        self.sub = self.create_subscription(
            CompressedImage, self.in_topic, self.on_img, qos)

        outs = []
        if self.pub_raw:  outs.append(self.out_base)
        if self.pub_comp: outs.append(self.out_comp)
        self.get_logger().info(f"Subscribed to {self.in_topic}")
        self.get_logger().info(f"Publishing to: {', '.join(outs) if outs else '(none)'}")

    def _publish_status(self, text: str):
        self.pub_status.publish(String(data=text))

    def _init_model(self):
        if not self.model_path:
            self.get_logger().warn(f"No --model given; defaulting to {DEFAULT_MODEL_PATH}")
            self.model_path = DEFAULT_MODEL_PATH
        if not os.path.exists(self.model_path):
            self.get_logger().warn(f"Model not found: {self.model_path}; will only republish frames.")
            self._publish_status("MODEL_MISSING republish_only")
            return
        if Interpreter is None:
            self.get_logger().error("No TFLite interpreter available on this system.")
            self._publish_status("MODEL_INIT_FAIL no_tflite")
            return

        delegate = None
        try:
            # Detect EdgeTPU lib and try to load delegate
            ctypes.CDLL('libedgetpu.so.1')
            delegate = load_delegate('libedgetpu.so.1')
            self.use_tpu = True
        except Exception as e:
            self.get_logger().warn(f"EdgeTPU not available: {e}")
            self.use_tpu = False

        try:
            if self.use_tpu and delegate is not None:
                self.interpreter = Interpreter(model_path=self.model_path,
                                               experimental_delegates=[delegate])
            else:
                self.interpreter = Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            inp = self.interpreter.get_input_details()[0]
            self.input_dtype = inp['dtype']             # usually uint8
            # input shape is [1,H,W,3]
            _, self.input_h, self.input_w, _ = inp['shape']
            self.get_logger().info(f"Model ready: {self.input_w}x{self.input_h}, dtype={self.input_dtype}, TPU={self.use_tpu}")
            self._publish_status(f"MODEL_READY TPU={self.use_tpu}")
        except Exception as e:
            self.get_logger().error(f"Failed to load model: {e}")
            self._publish_status(f"MODEL_INIT_FAIL {e}")

    def _maybe_rotate(self, img_rgb: np.ndarray) -> np.ndarray:
        if self.rotate_deg == 90:
            return np.rot90(img_rgb, 1)
        elif self.rotate_deg == 180:
            return np.rot90(img_rgb, 2)
        elif self.rotate_deg == 270:
            return np.rot90(img_rgb, 3)
        return img_rgb

    def _preprocess(self, img_rgb: np.ndarray) -> np.ndarray:
        # Resize with PIL (expects (W,H))
        pil = PILImage.fromarray(img_rgb)
        pil = pil.resize((self.input_w, self.input_h), resample=self.resample)
        arr = np.asarray(pil)
        if self.input_dtype == np.float32:
            arr = (arr.astype(np.float32) / 255.0)
        else:
            arr = arr.astype(self.input_dtype)
        return np.expand_dims(arr, axis=0)

    def _inference(self, img_rgb: np.ndarray):
        if self.interpreter is None:
            return None, None
        x = self._preprocess(img_rgb)
        t0 = time.time()
        self.interpreter.set_tensor(self.interpreter.get_input_details()[0]['index'], x)
        self.interpreter.invoke()
        ms = (time.time() - t0) * 1000.0
        out = self.interpreter.get_output_details()[0]
        y  = self.interpreter.get_tensor(out['index'])
        return y, ms

    def _publish_images(self, vis_rgb: np.ndarray, header):
        # Raw
        if self.pub_raw is not None:
            raw = Image()
            raw.header = header
            raw.height, raw.width = vis_rgb.shape[0], vis_rgb.shape[1]
            raw.encoding = 'rgb8'
            raw.is_bigendian = 0
            raw.step = raw.width * 3
            raw.data = vis_rgb.tobytes()
            self.pub_raw.publish(raw)
        # Compressed
        if self.pub_comp is not None:
            try:
                buf = BytesIO()
                PILImage.fromarray(vis_rgb).save(buf, format='JPEG', quality=self.jpeg_quality)
                cm = CompressedImage()
                cm.header = header
                cm.format = 'jpeg'
                cm.data = buf.getvalue()
                self.pub_comp.publish(cm)
            except Exception as e:
                self._publish_status(f"JPEG_ENCODE_FAIL {e}")

    def on_img(self, cmsg: CompressedImage):
        # Decode JPEG -> RGB (no OpenCV)
        try:
            pil = PILImage.open(BytesIO(cmsg.data)).convert('RGB')
            img_rgb = np.asarray(pil)
        except Exception as e:
            self._publish_status(f"DECODE_FAIL {e}")
            return

        # Optional orientation fix
        img_rgb = self._maybe_rotate(img_rgb)

        self.frame_count += 1
        vis_rgb = img_rgb
        inf_ms = None

        if self.interpreter is not None and (self.frame_count % self.every_n == 0):
            try:
                y, inf_ms = self._inference(img_rgb)  # y shape: [1,H,W,1] or [1,H,W]
                if y is not None:
                    y = np.squeeze(y)
                    # Normalize to [0,1]
                    y = (y - y.min()) / (y.max() - y.min() + 1e-6)
                    # Resize depth back to original image size for visualization
                    y_pil = PILImage.fromarray((y * 255).astype(np.uint8))
                    y_pil = y_pil.resize((img_rgb.shape[1], img_rgb.shape[0]), resample=self.resample)
                    depth_map = np.asarray(y_pil).astype(np.float32) / 255.0
                    vis_rgb = jet_colormap(depth_map)  # uint8 RGB
            except Exception as e:
                self._publish_status(f"INFER_FAIL {e}")

        # Publish
        self._publish_images(vis_rgb, cmsg.header)

        # Periodic status
        if inf_ms is not None:
            self._publish_status(f"RUN TPU={self.use_tpu} {inf_ms:.1f}ms")

def build_parser():
    p = argparse.ArgumentParser(description="Monocular depth on EdgeTPU (no OpenCV).")
    p.add_argument("--model", default=DEFAULT_MODEL_PATH,
                   help=f"Path to .tflite (default: {DEFAULT_MODEL_NAME} in script folder)")
    p.add_argument("--in", dest="in_topic", default=DEFAULT_IN_TOPIC,
                   help=f"Input compressed image topic (default: {DEFAULT_IN_TOPIC})")
    p.add_argument("--out", dest="out_base", default=DEFAULT_OUT_BASE,
                   help=f"Output base topic (raw); '/compressed' auto-added (default: {DEFAULT_OUT_BASE})")
    p.add_argument("--status", dest="status_topic", default=DEFAULT_STATUS,
                   help=f"Status topic (default: {DEFAULT_STATUS})")
    p.add_argument("--every-n", dest="every_n", type=int, default=DEFAULT_EVERY_N,
                   help=f"Run inference every N frames (default: {DEFAULT_EVERY_N})")
    p.add_argument("--publish", choices=("compressed","raw","both"), default=DEFAULT_PUBLISH,
                   help=f"Publish mode (default: {DEFAULT_PUBLISH})")
    p.add_argument("--jpeg-quality", type=int, default=DEFAULT_JPEG_QLTY,
                   help=f"JPEG quality 1-100 (default: {DEFAULT_JPEG_QLTY})")
    p.add_argument("--rotate", type=int, choices=(0,90,180,270), default=DEFAULT_ROTATE,
                   help=f"Rotate output by degrees (default: {DEFAULT_ROTATE})")
    p.add_argument("--resample", choices=("nearest","bilinear"), default=DEFAULT_RESAMPLE,
                   help=f"Resize filter for preprocess/upsample (default: {DEFAULT_RESAMPLE})")
    return p

def main():
    ap = build_parser()
    args = ap.parse_args()

    rclpy.init()
    node = MonoDepthTPU(args)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
