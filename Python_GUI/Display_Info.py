import pygame
import button as bt 
import Main as mn

class Display_Info(object):
	""" Class describing a device object and relevant """

	All = []

	def __init__(self, init_x, init_y, name = "Not Defined", setpoint = 0, unit = ' '):
		"""Add self to list of all objects"""
		self.All.append(self)
		"""Initialize variables from arguments"""
		self.unit = unit
		self.max_set   = 100
		self.setpoint  = setpoint
		self.measure   = 0
		self.loc_x     = init_x
		self.loc_y     = init_y
		self.name      = name
		"""Initialize de/increment variable to allow scrolling buttons"""
		self.increment  = False
		self.decrement  = False
		"""Initialize static text objects to be drawn"""
		self.inittext()
		"""Create up and down button objects"""
		self.upbuttonset = bt.Button(mn.Main.bgclr, init_x - 40 , init_y + 56, 30, 30, self, 'up')
		self.dwnbuttonme = bt.Button(mn.Main.bgclr, init_x -10, init_y + 56, 30, 30, self, 'down')



	@property
	def setpoint(self):
		return self.__setpoint

	@setpoint.setter
	def setpoint(self, setp):
		if setp < 0:
			self.__setpoint = 0
		elif setp > self.max_set:
			self.__setpoint = self.max_set
		else:
			self.__setpoint = setp

	@property
	def measure(self):
		return self.__measure

	@measure.setter
	def measure(self, meas):
		if meas < 0:
			self.__measure = 0
		elif meas > self.max_set:
			self.__measure = self.max_set
		else:
			self.__measure = meas

	@property
	def max_set(self):
		return self.__max_set

	@max_set.setter
	def max_set(self, x):
		self.__max_set = x

	def writetoscreen(self, screen):
		Line2 = self.txtfontlr.render(str(self.setpoint) + self.unit, True, self.txtclr)
		Line4 = self.txtfontlr.render(str(self.measure) + self.unit, True, self.txtclr)
		screen.blit(self.Line0, [self.loc_x-40, self.loc_y-15])
		screen.blit(self.Line1, [self.loc_x, self.loc_y+22])
		screen.blit(Line2, [self.loc_x + 40, self.loc_y + 44])
		screen.blit(self.Line3, [self.loc_x, self.loc_y + 88])
		screen.blit(Line4, [self.loc_x + 40, self.loc_y + 102])

	def inittext(self):
		self.txtclr    = (  0,   0,   0)
		self.txtfontsm = pygame.font.SysFont("Ubuntu", 22)
		self.txtfontlr = pygame.font.SysFont("Ubuntu", 44)
		self.txtfontmi = pygame.font.SysFont("Ubuntu", 33)
		self.Line0     = self.txtfontmi.render(self.name, True, self.txtclr)
		self.Line1     = self.txtfontsm.render("Setpoint", True, self.txtclr)
		self.Line3     = self.txtfontsm.render("Measure", True, self.txtclr)

	def checkIncrement(self):
		if self.increment:
			self.setpoint += 0.1
		elif self.decrement:
			self.setpoint -= 0.1



if __name__ == "__main__":
	print("Started running in Display_Info.py")
	execfile('Main.py')		