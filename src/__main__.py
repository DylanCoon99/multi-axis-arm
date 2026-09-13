#from src.test.test_j2_and_j3 import main
from src.robot.robot import Robot
#from src.test.test_stepper import main





def main():

	print("Running from main...")

	print("Testing instantiation of robot...")


	robot = Robot()

	#robot.move_to_angles(180, 45, 45)

	#robot.move_j1(90)
	#robot.move_j2(90)
	robot.move_j3(180)

	return





if __name__ == "__main__":
	main()