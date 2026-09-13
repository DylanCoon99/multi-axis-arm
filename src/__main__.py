#from src.test.test_j2_and_j3 import main
from src.robot.robot import Robot
#from src.test.test_stepper import main





def main():

	print("Running from main...")

	print("Testing instantiation of robot...")


	robot = Robot()

	robot.move_to_angles(180, 50, 100)

	return





if __name__ == "__main__":
	main()