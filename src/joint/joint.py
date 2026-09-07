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

	# need some kind of init to 

	def move_to(self, angle):
		pass


class ServoJoint(Joint):

	def move_to(self, angle):
		pass
