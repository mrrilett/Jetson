## Part 1: Basic Setup and Testing

This section covers installing the `xarm` package, setting up the environment, and performing basic tests to control the Jetson Robotic Arm.

### Verifying Installation
**Install the xArm Package**:

    py -m pip install xarm
    
This installs the `xarm` package for controlling the Jetson Arm’s servos. 

**Verify Installation**:
    
    py -m pip show xarm
    
Test the import in Python:

    import xarm
    print(xarm.__version__)  # Should print 0.2
    

### Hardware Setup

**Connect the xArm**: 
*   Connect the arm’s control board to your computer via USB (micro-USB to USB port).
*   Power the arm with the included (7.5V 6A DC) power supply.

### Basic Testing  
Create a new python file in VS Code and copy-paste the following sections of code. At the end, you should have a file with 6 lines.

1.  **Initialize the Controller**:
   

        import xarm
        arm = xarm.Controller('USB')  # Use 'USB' for USB connection
    
3.  **Move a Servo**: Move the gripper (servo ID 1):
    
        arm.setPosition(1, 500, 1000, True)  # Servo 1, position 500 (mid-range), 1000ms, wait=True
    Positions range from 0 to 1000 (~0–240 degrees).
    
5.  **Read Servo Position**:
    
        pos = arm.getPosition(1)
        print(f"Servo 1 position: {pos}")
    
6.  **Turn Off Servo**:
    
        arm.servoOff(1)
    


> Saftey Note: Test small movements to avoid servo strain. Ensure the arm is stable.

## Part 2: In-Depth Programming and Classes

This section explores the `xarm` package’s `Controller` class and methods for complex servo movements.

### Understanding the Controller Class

The `xarm.Controller` class controls the xArm’s six servos (5 joints, 1 gripper).

*   **Initialization**:
    
        import xarm
        arm = xarm.Controller('USB')
    
*   **Key Methods**:
    *   `setPosition(servo_id, position, time, wait)`: Move a servo to a position (0–1000) over `time` (ms).
    *   `getPosition(servo_id, degrees=False)`: Read position (0–1000 or degrees if `degrees=True`).
    *   `servoOff(servo_id)`: Disable a servo.
    *   `setPositions(positions, time, wait)`: Move multiple servos (implied in examples).

### Programming Servo Sequences

1.  **Capture Positions**: Manually move the arm and record positions:
    
        position = []
        for i in range(1, 7):  # Servos 1–6
            position.append(arm.getPosition(i))
        print(position)  # Example: [277, 497, 495, 545, 499, 489]
    
2.  **Execute a Sequence**: Move through predefined positions:
    
        import time
        arm_sequence = [
            [277, 497, 495, 545, 499, 489],  # Home, claw open
            [277, 497, 200, 835, 432, 498],  # Lower arm
            [699],                           # Close gripper
            [999.9, 497, 495, 545, 499, 489] # Back to home
        ]
        for positions in arm_sequence:
            if len(positions) == 1:
                arm.setPosition(1, positions[0], 1000, True)
            else:
                for i, pos in enumerate(positions, 1):
                    if pos != 999.9:
                        arm.setPosition(i, pos, 1000, True)
            time.sleep(0.5)
    

### Gripper Control

Control the gripper (servo ID 1):

    arm.setPosition(1, 277, 1000, True)  # Open
    arm.setPosition(1, 699, 1000, True)  # Close
    arm.servoOff(1)                     # Release

### Example: Simple Pick-and-Place

    import xarm
    from time import sleep
    
    arm = xarm.Controller('USB')
    # Home position
    arm.setPosition(1, 277, 1000, True)  # Open gripper
    arm.setPosition(2, 497, 1000, True)
    arm.setPosition(3, 495, 1000, True)
    arm.setPosition(4, 545, 1000, True)
    arm.setPosition(5, 499, 1000, True)
    arm.setPosition(6, 489, 1000, True)
    sleep(1)
    # Lower to pick
    arm.setPosition(3, 200, 1000, True)
    arm.setPosition(4, 835, 1000, True)
    arm.setPosition(5, 432, 1000, True)
    sleep(1)
    # Grab
    arm.setPosition(1, 699, 1000, True)
    sleep(0.5)
    # Lift
    arm.setPosition(3, 495, 1000, True)
    arm.setPosition(4, 545, 1000, True)
    arm.setPosition(5, 499, 1000, True)
    sleep(1)
    # Release
    arm.setPosition(1, 277, 1000, True)
    arm.servoOff(1)

### Best Practices

*   Use `time.sleep()` for smooth transitions.
*   Manually calibrate positions for accuracy (no built-in kinematics).
*   Verify movements with `getPosition`.

## Part 3: Advanced Coding

### Example: Vision-Guided Pick-and-Place

Integrate with OpenCV for vision control:

    import xarm
    import cv2
    import numpy as np
    from time import sleep
    
    arm = xarm.Controller('USB')
    cap = cv2.VideoCapture(0)
    arm.setPosition(1, 277, 1000, True)  # Open gripper
    arm.setPosition(2, 497, 1000, True)  # Home
    # ... (set other servos)
    while True:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([0, 120, 70]), np.array([10, 255, 255]))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            servo_pos = 497 + (x - 320) * 0.1  # Map to servo
            arm.setPosition(2, servo_pos, 1000, True)
            arm.setPosition(3, 200, 1000, True)
            arm.setPosition(1, 699, 1000, True)  # Grab
            sleep(0.5)
            arm.setPosition(3, 495, 1000, True)  # Lift
            break
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    arm.servoOff(1)


### Other Learning Resources

*   **GitHub**:
    *   [xArmServoController](https://github.com/ccourson/xArmServoController)
    *   [Hiwonder-LewanSoul-xArm-1S-Python-for-RPi-examples](https://github.com/DuaneOne/Hiwonder-LewanSoul-xArm-1S-Python-for-RPi-examples)
    *   [lewansoul-xarm](https://github.com/adeguet1/lewansoul-xarm) (ROS)
*   **Hiwonder Tutorials**: [Hiwonder Learn](https://www.hiwonder.com.cn/store/learn/42.html)
*   **Community**: [LewanSoul-xArm Enthusiast](https://www.facebook.com/xarmenthusiast)
