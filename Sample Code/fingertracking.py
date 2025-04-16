import xarm
import cv2
import numpy as np
from time import sleep

# Initialize xArm
try:
    arm = xarm.Controller('USB')  # Connect via USB
    print("xArm connected")
except Exception as e:
    print(f"Error connecting to xArm: {e}")
    exit(1)

# Initialize camera (WonderCam or webcam)
cap = cv2.VideoCapture(0)  # 0 for default camera (adjust if needed)
if not cap.isOpened():
    print("Error: Could not open camera")
    exit(1)

# Set camera resolution (adjust based on WonderCam specs)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Define red color range in HSV (for fingertip marker)
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

# Home position for xArm (servo IDs 1–6: gripper, base, shoulder, elbow, wrist, wrist rotation)
home_positions = [277, 497, 495, 545, 499, 489]  # Calibrated home
for i, pos in enumerate(home_positions, 1):
    arm.setPosition(i, pos, 1000, True)
sleep(1)

# Main loop for tracking and moving
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break

        # Convert frame to HSV for color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_red, upper_red)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours of red marker
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Get largest contour (assumed to be the fingertip marker)
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cx, cy = x + w // 2, y + h // 2  # Center of marker

            # Draw marker position on frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Map pixel coordinates to servo positions
            # Camera frame: x (0–640), y (0–480)
            # Servo 2 (base rotation): 0–1000 (~240°), center at 497
            # Servo 3 (shoulder): 200 (low) to 495 (home), adjust range
            servo2_pos = 497 + (cx - 320) * (500 / 320)  # Scale x to servo range
            servo3_pos = 495 - (cy - 240) * (295 / 240)  # Scale y to servo range
            servo2_pos = np.clip(servo2_pos, 0, 1000)  # Limit servo range
            servo3_pos = np.clip(servo3_pos, 200, 495)

            # Move xArm
            arm.setPosition(2, servo2_pos, 1000, True)  # Base rotation
            arm.setPosition(3, servo3_pos, 1000, True)  # Shoulder
            print(f"Fingertip at ({cx}, {cy}), Servo 2: {servo2_pos}, Servo 3: {servo3_pos}")

        # Display frame
        cv2.imshow('Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program terminated by user")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Return to home and release resources
    for i, pos in enumerate(home_positions, 1):
        arm.setPosition(i, pos, 1000, True)
    arm.servoOff(1)  # Release gripper
    cap.release()
    cv2.destroyAllWindows()
    print("Cleanup complete")
