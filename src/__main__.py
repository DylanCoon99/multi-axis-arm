#from src.test.test_j2_and_j3 import main
from src.robot.robot import Robot
#from src.test.test_stepper import main
from src.test.test_gripper import main
import time



def main():

	print("Running from main...")

	print("Testing instantiation of robot...")


	robot = Robot()

	#robot.move_to_angles(180, 45, 45)

	'''
	robot.move_j1(-90)
	time.sleep(1)
	robot.move_j2(120)
	time.sleep(1)
	robot.move_j3(90)
	'''
	robot.move_gripper(90)

	return





if __name__ == "__main__":
	main()