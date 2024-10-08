
from xarm import version
from xarm.wrapper import XArmAPI

ip = '192.168.1.232'

arm = XArmAPI(ip)

arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

speed = 100
# arm.move_gohome(wait=True)

arm.set_servo_angle(angle=[-45, 0,-20, 0,0,0], speed=speed/2)

arm.set_servo_angle(angle=[45, 0,-20, 0,0,0], speed=speed)

arm.disconnect()