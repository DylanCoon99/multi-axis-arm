from src.joint import StepperJoint, ServoJoint
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
		self.joints = []
		self.logger = logging.getLogger(__name__)

		# Configures the root logger globally
		logging.basicConfig(
			level=logging.INFO,
			format="%(asctime)s - %(levelname)s - %(message)s",
			handlers=[logging.StreamHandler()]
		)

		self.logger.info(f"Initializing Robot with {config}...")

		# instantiate a robot as a list of joints
		# config from the yaml file path
		

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



