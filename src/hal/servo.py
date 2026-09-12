from adafruit_servokit import ServoKit

# this is the file that will interface with the servos
# this will be transparent to my main code


def servo_kit_setup(channels, address):

	# somehow need to pass the pins that servos are on to this function;
	# for now they will be hardcoded

	kit = ServoKit(channels=channels, address=address)

    # Per-servo calibration offsets (adjust until both agree at 90°)

    # effective range: 36 -> 180
    # effective range accounting for arm geometry: 36 -> 150


    J2_OFFSET_14 = 0
    J2_OFFSET_15 = 35

    kit.servo[13].set_pulse_width_range(500, 2500)
    kit.servo[13].actuation_range = 180

    kit.servo[14].set_pulse_width_range(500, 2500)
    kit.servo[14].actuation_range = 180

    kit.servo[15].set_pulse_width_range(500, 2500)
    kit.servo[15].actuation_range = 180

	return kit


def move_servo_to(kit, servo, angle):
	kit.servo[servo].angle = angle
	return


def servo_reset(kit):

	kit.servo[13].angle = 0
	kit.servo[14].angle = 65
	kit.servo[15].angle = 65

	return