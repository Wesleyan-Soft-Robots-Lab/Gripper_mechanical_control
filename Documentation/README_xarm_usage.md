Initial Notes

The xArm is extraordinarily sensitive to close movements and will often fail if joints are moved to an improper position. The method to prevent this is still unclear and requires further testing to conclude the necessary bounds.
Issues with movement can often be resolved by making adjustments in the UFACTORY software.



1. NETWORK AND HARDWARE CONFIGURATION (Lab Computers)

To configure the IP settings for the arm on lab computers:
Go to Settings > Network & Internet.
Click Edit under IP Assignment.
Choose Manual and enable IPv4.
Enter 192.168.1.100 as the IP address.
Enter 255.255.255.0 as the Subnet mask.

On the physical device make sure to:

Plug in the Network Cable and Power Cord:
<img src="xarm_img\xarm_cables.jpg" alt="Picture of Cords">

Turn on the Xarm using the Red Power Button (currently off below): 
<img src="xarm_img\xarm_powerswitch.jpg" alt="Picture of Power Button">

2. IMPORT NECESSARY LIBRARIES

It is necessary to include the appropriate import in your script to enable API controls: from xarm.wrapper import XArmAPI.
It is also beneficial to include time and serial if your work involves timed intervals or movement controlled by external tools like an Arduino.


3. CONNECTING TO THE XARM

Begin by assigning a string IP address such as ip = '192.168.1.232'.
Use the IP to configure and initialize the arm with arm = XArmAPI(ip).


4. ENABLING AND INITIALIZING XARM

Enabling the motors involves arm.motion_enable(enable=True), where only True or False are valid inputs; True is necessary to allow movement.
Setting the mode with arm.set_mode(0) puts the arm in position control mode, although further investigation is needed for other control modes such as velocity or force.
Setting the state with arm.set_state(state=0) places the arm in a ready state. Other states include 3 for pause and 4 for stop.


5. SPEED/ANGLE CONFIGURATION

A movement speed can be set with speed = 100, which is comparable to human reaction time. Speeds over 100 can cause the arm to shake if not anchored properly and could pose a hazard.
The angle variable is defined as a list of six values representing the six rotational axes (joints) of the arm, e.g., angle = [0, 0, 0, 0, 0, 0] for the home position.
Avoid using values over 359.9 degrees as this could prevent the arm from resetting properly. Values above 360 degrees will trigger an out-of-bounds error.

The corresponding angles are correspond to the following joints:
<img src="xarm_img\xarm_img1.jpg" alt="Xarm Servos 1">
<img src="xarm_img\xarm_img2.jpg" alt="Xarm Servos 2">

The following images give a general idea of the direction according to the angles of the servos:
<img src="xarm_img\Servo1&2.jpg" alt="Servo 1 and 2">

<img src="xarm_img\Servo3.jpg" alt="Servo 3">

<img src="xarm_img\Servo4.jpg" alt="Servo 4">

<img src="xarm_img\Servo5.jpg" alt="Servo 5">

<img src="xarm_img\Servo6.jpg" alt="Servo 6">


6. IMPORTANT CONSIDERATION FOR MOVEMENT

The xArm does not optimize the sequence of movements if multiple joints are moved simultaneously, which may cause joints to become stuck or fail to execute movements correctly. For example, moving from [0, 0, 0, 0, 0, 0] to [0, 30, 90, 0, 0, 0] may cause interference if joints moving to 30 and 90 degrees lock up.
Ensure that movements do not exceed joint limits and avoid simultaneous complex movements.


7. MOVEMENT COMMANDS

Move to the home position using arm.move_gohome(speed=speed, wait=True)
* The above images in (5) depict the arm in home positions ( [0,0,0,0,0,0] )

Set servo angles with arm.set_servo_angle(angle=angle, speed=speed, wait=True).
where wait allow for a slight delay before movements

Get servo angles with arm.get_servo_angle(); add is_radian=True to get the angles in radians if needed.


Always disconnect the arm at the end of your script to ensure safe operation using arm.disconnect().


8. CARTESIAN COORDINATE USAGE

The Cartesian functionality of the Xarm is difficult to grasp because the 3 dimensional space it operates is a bit confusing.  

Regardless, to utilizes the functions this supports we can use the same general setup in steps 1 - 4 (and speed from 5).
The major components are are X, Y and Z coordinates.  Additionally want to Set the roll, pitch and yaw which set the machine in 3 dimensional space.

There are 2 primary movement functions we can utilize:

arm.set_position(x, y, z, roll, pitch, yaw, speed, wait);  which works the same set servo position but sets it in 3 dimensional space rather than according to the angle of the motors.

arm.move_circle(intial_pose, end_pose, percent, speed); which takes a starting pose and in a circular motions moves to the final position.  In this case percent would symbolize how closely the arm follows the circumference of the circle.

