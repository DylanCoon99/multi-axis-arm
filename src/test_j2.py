import sys
import time
from adafruit_servokit import ServoKit







def main():
    kit = ServoKit(channels=16, address=0x40)

    # Per-servo calibration offsets (adjust until both agree at 90°)

    # effective range: 36 -> 180
    # effective range accounting for arm geometry: 36 -> 150


    J2_OFFSET_14 = 0
    J2_OFFSET_15 = 36

    kit.servo[14].set_pulse_width_range(500, 2500)
    kit.servo[14].actuation_range = 180

    kit.servo[15].set_pulse_width_range(500, 2500)
    kit.servo[15].actuation_range = 180

    # Usage: python test_j2.py <channel> <angle>
    #   e.g. python test_j2.py 14 90
    #        python test_j2.py 15 90
    #        python test_j2.py both 90  (only after calibration!)
    if len(sys.argv) < 3:
        print("Usage: python test_j2.py <14|15|both> <angle>")
        print("  Test one servo at a time first to find offsets.")
        print(f"  Current offsets: servo 14 = {J2_OFFSET_14}, servo 15 = {J2_OFFSET_15}")
        return

    target = sys.argv[1]
    angle = float(sys.argv[2])

    if target == "14":
        cmd = angle + J2_OFFSET_14
        print(f"Servo 14 -> {cmd}°")
        kit.servo[14].angle = cmd
    elif target == "15":
        cmd = (180 - angle) + J2_OFFSET_15
        print(f"Servo 15 -> {cmd}° (mirrored from {angle}°)")
        kit.servo[15].angle = cmd
    elif target == "both":
        cmd_14 = angle + J2_OFFSET_14
        cmd_15 = (180 - angle) + J2_OFFSET_15
        print(f"Servo 14 -> {cmd_14}°, Servo 15 -> {cmd_15}° (mirrored)")
        kit.servo[14].angle = cmd_14
        kit.servo[15].angle = cmd_15
    else:
        print("First argument must be 14, 15, or both")
        return

    time.sleep(1)
    print("Done.")
