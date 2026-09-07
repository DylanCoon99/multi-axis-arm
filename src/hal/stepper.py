from tmc_driver import Tmc2209, TmcEnableControlToff, TmcMotionControlStepDir
from tmc_driver.com import TmcComUart
from time import sleep

# GPIO 17: RX (Pi TX -> 1kΩ resistor -> TMC2209 PDN_UART)
# GPIO 27: TX (not used for single-wire UART, but reserved)
# GPIO 22: STEP
# GPIO 5:  DIR
# EN: tied LOW (always enabled)

STEP_PIN = 22
DIR_PIN = 5
UART_PORT = "/dev/ttyAMA0"

# Motor specs: Anet 42SHDC3025-24B
# Rated current: 0.9A per phase
# Target: 70% = 630mA RMS
CURRENT_RMS_MA = 630


# define the stepper interface here


'''

def main():
    tmc = Tmc2209(
        TmcEnableControlToff(),
        TmcMotionControlStepDir(STEP_PIN, DIR_PIN),
        TmcComUart(UART_PORT),
    )

    try:
        # Re-enable motor output in case previous run left it disabled
        tmc.set_motor_enabled(True)

        # Configure driver via UART
        tmc.set_current_rms(CURRENT_RMS_MA)
        tmc.set_microstepping_resolution(16)
        tmc.set_interpolation(True)        # interpolate to 256 microsteps
        tmc.set_spreadcycle(False)          # StealthChop (quiet mode)

        # Motion parameters (in full steps)
        tmc.acceleration_fullstep = 500
        tmc.max_speed_fullstep = 200

        print("Driver configured:")
        print(f"  Current: {CURRENT_RMS_MA} mA RMS")
        print(f"  Microstepping: 1/16 (interpolated to 256)")
        print(f"  Mode: StealthChop")
        print()

        STEPS_PER_REV = 200 * 16  # 3200 microsteps per revolution at 1/16

        # Test 1: One full revolution
        print("Test 1: Rotating 1 revolution forward...")
        tmc.run_to_position_steps(STEPS_PER_REV)
        sleep(1)

        # Test 2: Return to start
        print("Test 2: Returning to start...")
        tmc.run_to_position_steps(0)
        sleep(1)

        # Test 3: Two full revolutions
        print("Test 3: Rotating 2 revolutions forward...")
        tmc.run_to_position_steps(STEPS_PER_REV * 2)
        sleep(1)

        print("Test 3: Returning to start...")
        tmc.run_to_position_steps(0)
        sleep(1)

        print("All tests complete.")

    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        tmc.set_motor_enabled(False)
        tmc.deinit()
        print("Motor disabled.")


if __name__ == "__main__":
    main()
'''