import time
from adafruit_servokit import ServoKit


def sweep(channel, start, end, step=1.0, delay=0.02):
    direction = 1 if end > start else -1
    angle = start
    while (angle - end) * direction < 0:
        set_angle(channel, angle)
        angle += step * direction
        time.sleep(delay)
    set_angle(channel, end)


def main():
    kit = ServoKit(channels=16, address=0x40)

    SERVO = 0    # PCA9685 channel index for the pan axis
    #PAN = 1   # PCA9685 channel index for the tilt axis

    # Calibrate to the specific servo. Many hobby servos require a wider
    # range than the library default of 750-2250 us to reach full travel.
    kit.servo[SERVO].set_pulse_width_range(500, 2500)
    kit.servo[SERVO].actuation_range = 180

    for i in range(3):
	    kit.servo[SERVO].angle = 180     # center
	    time.sleep(1)
	    kit.servo[SERVO].angle = 90     # center
	    time.sleep(1)
	    kit.servo[SERVO].angle = 180