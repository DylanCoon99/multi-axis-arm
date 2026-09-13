from src.joint.joint import StepperJoint, ServoJoint, DualServoJoint
from src.config.config import RobotConfig, StepperConfig, DualServoConfig, ServoConfig
from src.hal.servo import servo_kit_setup, servo_reset
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

	def __init__(self, config="/home/dymco99/Documents/programs/robotic-arm/src/config/example_config.yaml"):
		self.state = None
		self.logger = logging.getLogger(__name__)
		self.joints = []
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
		self.servo_kit = servo_kit_setup(16, self.config.pca9685_address)
		servo_reset(self.servo_kit)

		self.J1 = StepperJoint(self.config.j1)
		self.J2 = DualServoJoint(self.config.j2, self.servo_kit)
		self.J3 = ServoJoint(self.config.j3, self.servo_kit)
		

	def home(self):
		# moves robot to home position
		pass

	def current_state(self):
		# returns the robots current state
		return self.state

	def move_to_angles(self, a1, a2, a3):
		# moves the robot joints to each angle respectively
		#self.J1.move_to(a1)
		self.J2.move_to(a2)
		#self.J3.move_to(a3)

		# update the robot state

	def move_j1(self, a):
		self.J1.move_to(a)

	def move_j2(self, a):
		self.J2.move_to(a)

	def move_j3(self, a):
		self.J3.move_to(a)
	
	def move_to_target(self, point: Point):
		# TODO: utilizes inverse kinematics to move manipulator to the target point
		pass

	def is_reachable(self, point: Point) -> bool:
		# TODO: returns true if point is reachable; false otherwise
		pass




