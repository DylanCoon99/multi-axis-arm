from dataclasses import dataclass
import yaml


@dataclass
class StepperConfig:
	step_pin: int
	dir_pin: int
	uart_port: str
	current_rms_ma: int
	microstepping: int
	gear_ratio: float
	min_angle: float
	max_angle: float


@dataclass
class DualServoConfig:
	pca9685_channels: list
	pulse_range: tuple
	actuation_range: int
	offset_14: int
	offset_15: int
	min_angle: float
	max_angle: float


@dataclass
class ServoConfig:
	pca9685_channel: int
	pulse_range: tuple
	actuation_range: int
	min_angle: float
	max_angle: float


@dataclass
class RobotConfig:
	j1: StepperConfig
	j2: DualServoConfig
	j3: ServoConfig
	gripper: ServoConfig
	pca9685_address: int

	@staticmethod
	def from_yaml(path: str) -> "RobotConfig":
		with open(path, "r") as f:
			cfg = yaml.safe_load(f)

		joints = cfg["joints"]

		j1 = StepperConfig(
			step_pin=joints["J1"]["step_pin"],
			dir_pin=joints["J1"]["dir_pin"],
			uart_port=joints["J1"]["uart_port"],
			current_rms_ma=joints["J1"]["current_rms_ma"],
			microstepping=joints["J1"]["microstepping"],
			gear_ratio=joints["J1"]["gear_ratio"],
			min_angle=joints["J1"]["min_angle"],
			max_angle=joints["J1"]["max_angle"],
		)

		j2 = DualServoConfig(
			pca9685_channels=joints["J2"]["pca9685_channels"],
			pulse_range=tuple(joints["J2"]["pulse_range"]),
			actuation_range=joints["J2"]["actuation_range"],
			offset_14=joints["J2"]["offset_14"],
			offset_15=joints["J2"]["offset_15"],
			min_angle=joints["J2"]["min_angle"],
			max_angle=joints["J2"]["max_angle"],
		)

		j3 = ServoConfig(
			pca9685_channel=joints["J3"]["pca9685_channel"],
			pulse_range=tuple(joints["J3"]["pulse_range"]),
			actuation_range=joints["J3"]["actuation_range"],
			min_angle=joints["J3"]["min_angle"],
			max_angle=joints["J3"]["max_angle"],
		)

		gripper = ServoConfig(
			pca9685_channel=joints["gripper"]["pca9685_channel"],
			pulse_range=tuple(joints["gripper"]["pulse_range"]),
			actuation_range=joints["gripper"]["actuation_range"],
			min_angle=joints["gripper"]["min_angle"],
			max_angle=joints["gripper"]["max_angle"],
		)

		return RobotConfig(
			j1=j1,
			j2=j2,
			j3=j3,
			gripper=gripper,
			pca9685_address=cfg["pca9685"]["address"],
		)