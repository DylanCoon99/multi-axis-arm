from src.joint import StepperJoint, ServoJoint
from src.config.config import RobotConfig, StepperConfig, DualServoConfig, ServoConfig
from dataclasses import dataclass
import logging


@dataclass
class Point:
	x: float
	y: float
	z: float

@dataclass
class State:
	j1_angle: float
	j2_angle: float
	j3_angle: float


class Robot:

	def __init__(self, config="/Users/Dylan/Documents/robotic-arm/src/config/config.yaml"):
		self.state = None
		self.logger = logging.getLogger(__name__)

		# Configures the root logger globally
		logging.basicConfig(
			level=logging.INFO,
			format="%(asctime)s - %(levelname)s - %(message)s",
			handlers=[logging.StreamHandler()]
		)

		self.logger.info(f"Initializing Robot with {config}...")

		# parse the yaml into a RobotConfig
		self.config = RobotConfig.from_yaml(config)

		# servo driver kit needs to be instantiate here because it is shared between mutliple joints
		self.servo_kit = servo_kit_setup(self.pca9685.channels, self.pca9685.address)
		servo_reset(self.servo_kit)

		# instantiate all the joints
		self.J1 = StepperJoint(self.config.StepperConfig)
		self.J2 = ServoJoint(self.config.DualServoConfig, self.servo_kit)
		self.J3 = ServoJoint(self.config.ServoConfig, self.servo_kit)
		

	def home(self):
		# moves robot to home position
		pass

	def current_state(self):
		# returns the robots current state
		return self.state

	def move_to_angles(self, a1, a2, a3):
		# moves the robot joints to each angle respectively
		pass

	def move_to_target(self, point: Point):
		# utilizes inverse kinematics to move manipulator to the target point
		pass

	def is_reachable(self, point: Point) -> bool:
		# returns true if point is reachable; false otherwise
		pass




