import xarm
import cv2
import mediapipe as mp
import numpy as np
from time import sleep

# Initialize xArm
try:
    arm = xarm.Controller('USB')  # Connect via USB
    print("xArm connected")
except Exception as e:
    print(f"Error connecting to xArm: {e}")
    exit(1)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize camera (WonderCam or webcam)
cap = cv2.VideoCapture(0)  # 0 for default camera (adjust if needed)
if not cap.isOpened():
    print("Error: Could not open camera")
    exit(1)

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Home position for xArm (servo IDs 1–6: gripper, base, shoulder, elbow, wrist, wrist rotation)
home_positions = [277, 497, 495, 545, 499, 489]  # Calibrated home
for i, pos in enumerate(home_positions, 1):
    arm.setPosition(i, pos, 1000, True)
sleep(1)

# Gripper control parameters
GRIPPER_OPEN = 277   # Open position (0–1000 scale)
GRIPPER_CLOSED = 699 # Closed position
DISTANCE_THRESHOLD_OPEN = 50  # Pixel distance for open gripper
DISTANCE_THRESHOLD_CLOSE = 20 # Pixel distance for closed gripper
gripper_state = 'open'       # Track gripper state

# Main loop for tracking and moving
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break

        # Flip frame for natural orientation
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame with MediaPipe
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get thumb (landmark 4) and index (landmark 8) coordinates
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]

                # Convert normalized coordinates to pixel values
                h, w, _ = frame.shape
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

                # Calculate distance between thumb and index finger
                distance = np.sqrt((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2)

                # Control gripper based on distance
                if distance > DISTANCE_THRESHOLD_OPEN and gripper_state != 'open':
                    arm.setPosition(1, GRIPPER_OPEN, 1000, True)
                    gripper_state = 'open'
                    print("Gripper: Open")
                elif distance < DISTANCE_THRESHOLD_CLOSE and gripper_state != 'closed':
                    arm.setPosition(1, GRIPPER_CLOSED, 1000, True)
                    gripper_state = 'closed'
                    print("Gripper: Closed")

                # Map index fingertip to servo positions
                # Camera frame: x (0–640), y (0–480)
                # Servo 2 (base rotation): 0–1000 (~240°), center at 497
                # Servo 3 (shoulder): 200 (low) to 495 (home)
                servo2_pos = 497 + (index_x - 320) * (500 / 320)  # Scale x
                servo3_pos = 495 - (index_y - 240) * (295 / 240)  # Scale y
                servo2_pos = np.clip(servo2_pos, 0, 1000)
                servo3_pos = np.clip(servo3_pos, 200, 495)

                # Move xArm
                arm.setPosition(2, servo2_pos, 1000, True)  # Base rotation
                arm.setPosition(3, servo3_pos, 1000, True)  # Shoulder
                print(f"Index fingertip at ({index_x}, {index_y}), Servo 2: {servo2_pos}, Servo 3: {servo3_pos}")

                # Draw thumb and index points
                cv2.circle(frame, (thumb_x, thumb_y), 5, (0, 0, 255), -1)
                cv2.circle(frame, (index_x, index_y), 5, (0, 255, 0), -1)

        # Display frame
        cv2.imshow('Hand Tracking', frame)
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
