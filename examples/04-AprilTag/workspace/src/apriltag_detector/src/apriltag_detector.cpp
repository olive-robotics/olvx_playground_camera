// -*-c++-*---------------------------------------------------------------------------------------
// Copyright 2024 Bernd Pfrommer <bernd.pfrommer@gmail.com>
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <apriltag_detector/apriltag_detector.hpp>
#include <array>

#include <opencv2/imgcodecs.hpp> // For decoding compressed images
#include <apriltag_detector/detector_wrapper.hpp>
#include <opencv2/core/core.hpp>
#include <rclcpp_components/register_node_macro.hpp>

namespace apriltag_detector
{
ApriltagDetector::ApriltagDetector(const rclcpp::NodeOptions & options)
: Node(
    "apriltag_detector",
    rclcpp::NodeOptions(options)
      .automatically_declare_parameters_from_overrides(true))
{
  detector_.reset(new DetectorWrapper(
    get_parameter_or("tag_family", std::string("tf36h11")),
    get_parameter_or<int>("max_hamming_distance", 0)));
  detector_->setDecimateFactor(get_parameter_or("decimate_factor", 1.0));
  detector_->setQuadSigma(get_parameter_or("blur", 0.0));
  detector_->setNumberOfThreads(get_parameter_or("num_threads", 1));
  get_parameter_or(
    "image_qos_profile", imageQoSProfile_, std::string("sensor_data"));

  // publish images using standard ROS 2 publisher with sensor_data QoS
  auto qos = rclcpp::SensorDataQoS();
  imagePub_ = this->create_publisher<sensor_msgs::msg::CompressedImage>("/tags/compressed", qos);
  // publish detections with sensor_data QoS
  detectPub_ = this->create_publisher<ApriltagArray>("/tags", qos);

  // Adjusted subscription creation
  imageSub_ = this->create_subscription<sensor_msgs::msg::CompressedImage>(
    "/olive/camera/id01/image/compressed", qos, std::bind(&ApriltagDetector::callback, this, std::placeholders::_1));
  // Standard ROS 2 subscription for compressed image messages with sensor_data QoS
 
}

ApriltagDetector::~ApriltagDetector()
{
  
}

rmw_qos_profile_t string_to_profile(const std::string & s)
{
  if (s == "sensor_data") {
    return (rmw_qos_profile_sensor_data);
  }
  return (rmw_qos_profile_default);
}

void ApriltagDetector::subscriptionCheckTimerExpired()
{
 
}

void ApriltagDetector::callback(const sensor_msgs::msg::CompressedImage::SharedPtr msg)
{
  apriltag_msgs::msg::AprilTagDetectionArray arrayMsg;
  cv::Mat cvImg;
 
  try {
    // Decode the compressed image
    std::vector<uint8_t> imgData(msg->data.begin(), msg->data.end());
    cvImg = cv::imdecode(imgData, cv::IMREAD_GRAYSCALE);
  } catch (const cv::Exception& e) {
    RCLCPP_WARN(this->get_logger(), "Could not decode image: %s", e.what());
    return;
  }

  if (!cvImg.empty()) {
    detector_->detect(cvImg, &arrayMsg);
  } else {
    RCLCPP_WARN(this->get_logger(), "Received an empty image.");
    return;
  }
  
  arrayMsg.header = msg->header;
  detectPub_->publish(arrayMsg);
  
  cv::Mat colorImg = DetectorWrapper::draw(cvImg, arrayMsg); // Ensure this method exists and works as expected
	
  std::vector<uint8_t> buffer;
  cv::imencode(".jpg", colorImg, buffer);
  auto pubImg = sensor_msgs::msg::CompressedImage();
  pubImg.header = msg->header; // Copy header for consistency
  pubImg.format = "jpeg"; // Set format to match encoding
  pubImg.data = buffer; // Assign compressed data
  imagePub_->publish(pubImg); // Publish the compressed image

}

}  // namespace apriltag_detector

RCLCPP_COMPONENTS_REGISTER_NODE(apriltag_detector::ApriltagDetector)
