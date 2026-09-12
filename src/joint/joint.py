from abc import ABC, abstractmethod

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
		STEP_PIN = config.step_pin
		DIR_PIN = config.dir_pin
		UART_PORT = config.uart_port
		CURRENT_RMS_MA = config.current_rms_ma

		self.tmc = Tmc2209(
			TmcEnableControlToff(),
			TmcMotionControlStepDir(STEP_PIN, DIR_PIN),
			TmcComUart(UART_PORT),
		)

		self.current_rms_ma = CURRENT_RMS_MA

	def move_to(self, angle):
		pass


class ServoJoint(Joint):

	def __init__(self, config, kit):

		# need to check what kind of servo joint this is (single or dual)
		self.channel = config.pca9685_channel
		self.kit = kit  # shared ServoKit instance 

	def move_to(self, angle):
		self.kit.servo[self.channel].angle = angle


