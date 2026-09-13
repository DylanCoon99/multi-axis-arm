from abc import ABC, abstractmethod
from tmc_driver import Tmc2209, TmcEnableControlToff, TmcMotionControlStepDir
from tmc_driver.com import TmcComUart

# import the HAL interface -> 

# define the joint interface


# Joint: Abstract Class
class Joint(ABC):

	# An abstract method (subclasses MUST implement this)
	@abstractmethod
	def move_to(self, angle):
		pass


class StepperJoint(Joint):
	def __init__(self, config):
		self.step_pin = config.step_pin
		self.dir_pin = config.dir_pin
		self.uart_port = config.uart_port
		self.current_rms_ma = config.current_rms_ma
		self.microstepping = config.microstepping
		self.gear_ratio = config.gear_ratio

		self.tmc = Tmc2209(
			TmcEnableControlToff(),
			TmcMotionControlStepDir(self.step_pin, self.dir_pin),
			TmcComUart(self.uart_port),
		)

		self.tmc.set_motor_enabled(True)
		self.tmc.set_microstepping_resolution(self.microstepping)
		self.tmc.set_interpolation(True)        # interpolate to 256 microsteps
		self.tmc.set_spreadcycle(False)          # StealthChop (quiet mode)

		# Motion parameters (in full steps)
		self.tmc.acceleration_fullstep = 500
		self.tmc.max_speed_fullstep = 200
		self.steps_per_revolution = 200 * 16

		self.steps_per_degree = (200 * self.microstepping * self.gear_ratio) / 360

	def move_to(self, angle):
		steps = self._angle_to_steps(angle)
		tmc.run_to_position_steps(steps)
		return


	def _angle_to_steps(angle):
		# TODO: IMPLEMENT
		steps = angle * self.steps_per_degree
		return steps
		


class ServoJoint(Joint):

	def __init__(self, config, kit):
		self.channel = config.pca9685_channel
		self.kit = kit  # shared ServoKit instance 

	def move_to(self, angle):
		self.kit.servo[self.channel].angle = angle


class DualServoJoint(Joint):

	def __init__(self, config, kit):

		self.channels = config.pca9685_channels
		self.kit = kit  # shared ServoKit instance 

		self.offset_14 = config.offset_14
		self.offset_15 = config.offset_15

	def move_to(self, angle):
		#self.kit.servo[self.channel].angle = angle

		cmd_14 = angle + self.offset_14
		cmd_15 = (180 - angle) + self.offset_15
		kit.servo[self.channels[0]].angle = cmd_14
		kit.servo[self.channels[1]].angle = cmd_15


