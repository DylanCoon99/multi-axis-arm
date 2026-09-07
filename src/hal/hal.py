from dataclasses import dataclass
from src.hal.servo import servo_reset, servo_kit_setup

'''
This is where the hardware abstraction layer (hal) will be defined

Hardware to support
	- 1 nema 17 stepper motor with Tmc2209 driver
	- 3 mg996r servo motors using adafruit servo kit


'''


# I am thinking of having a hardware config class that stores the driver interfaces and servo kit

class HardwareConfig:

	def __init__(self, channels=16, address=0x40, STEP_PIN, DIR_PIN, UART_PIN, CURRENT_RMS_MA= 630):

		self.servo_kit = servo_kit_setup(self.channels, self.address)
		servo_reset(self.servo_kit)

		self.tmc = Tmc2209(
	        TmcEnableControlToff(),
	        TmcMotionControlStepDir(STEP_PIN, DIR_PIN),
	        TmcComUart(UART_PORT),
	    )

	    self.current_rms_ma = CURRENT_RMS_MA

		return


