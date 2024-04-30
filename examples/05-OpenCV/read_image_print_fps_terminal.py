import cv2
import time

# Open the camera device
cap = cv2.VideoCapture(0)  # Changed to 1 for /dev/video1

# Check if the camera opened successfully
if not cap.isOpened():
    print('Error: Could not open camera.')
    exit()

# Set the video frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Set the video codec to MJPG and the frame rate to 120fps
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FPS, 120)

frame_count = 0
start_time = time.time()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    # Break the loop if frame reading was not successful
    if not ret:
        print('Failed to grab frame.')
        break
    
    # Display the frame (optional)
    cv2.imshow('Frame', frame)
    
    frame_count += 1
    elapsed_time = time.time() - start_time
    
    if elapsed_time >= 1.0:  # One second has passed
        avg_fps = frame_count / elapsed_time
        print(f'Average FPS: {avg_fps}')
        frame_count = 0
        start_time = time.time()
    
    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

