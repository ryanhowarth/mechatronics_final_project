
import Robot
from time import sleep


PWM_L = 12
INPUT_1_LEFT = 8
INPUT_2_LEFT = 25

PWM_R = 13
INPUT_1_RIGHT = 11
INPUT_2_RIGHT = 9

SERVO_LIFT = 0
SERVO_PINCH = 7

myRobot = Robot.robot(INPUT_1_LEFT, INPUT_2_LEFT, PWM_L, INPUT_1_RIGHT, INPUT_2_RIGHT, PWM_R, SERVO_LIFT, SERVO_PINCH)

while True:
    '''
    myRobot.moveForward()
    sleep(2)

    myRobot.turnLeft()
    sleep(2)

    myRobot.turnRight()
    sleep(2)

    myRobot.turnAround()
    sleep(2)

    myRobot.stop()
    sleep(2)

    myRobot.pickupGift()
    sleep(2)

    myRobot.dropGift()
    sleep(2)
    '''
    print myRobot.getIrSensorData()
    sleep(1)
