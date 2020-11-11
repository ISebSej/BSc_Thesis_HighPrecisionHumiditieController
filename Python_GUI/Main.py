import pygame
import pygame.locals as pg
import serial
import time
import button as bt 
import threading
import BronkhorstDevices as bronk
import queue
import Display_Info as disin

class Main(object):
	"""The Main Object containing the game"""
	bgclr   = 	(176,196,222)

	def __init__(self):
		
		self.screen  = pygame.display.get_surface()
		self.running = True
		self.width   = 800
		self.height  = 600
		self.fps     = 60
		self.main()

	def main(self):

		"""Initialize pygame display"""
		pygame.init()
		self.surface = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Humidity Controller')
		self.surface.fill(self.bgclr)

		"""Create temperature and humidity objects"""
		Temp  = disin.Display_Info(50, 50, "Temperature", 21, "C")
		Humi  = disin.Display_Info(325, 50, "Humidity", 0 , "%")
		Mass  = disin.Display_Info(600, 50, "Massflow", 0 , "g/h")

		Test1 = bronk.MainDeviceClass(50, 300)
		Test2 = bronk.MainDeviceClass(325, 300)
		Test3 = bronk.MainDeviceClass(600, 300)
		"""Main loop"""
		while self.running:
			"""Setup for main loop"""
			start = time.time()
			self.surface.fill(self.bgclr)
			"""Draw all Display info objects"""
			for textobject in disin.Display_Info.All:
				textobject.writetoscreen(self.surface)
				if textobject.increment:
					textobject.setpoint += 0.1
				elif textobject.decrement:
					textobject.setpoint -= 0.1
			"""Draw all buttons to screen"""
			for button in bt.Button.All:
				button.draw(self.surface)

			for device in bronk.MainDeviceClass.All:
				device.writetoscreen(self.surface)
			"""Finalize main loop"""
			time.sleep(max(1./self.fps - (time.time() - start), 0))
			pygame.display.update() 
			for event in pygame.event.get():
				if event.type == pg.QUIT:
					self.running = False
				if event.type == pg.MOUSEBUTTONDOWN:
					for button in bt.Button.All:
						if button.isOver(event.pos) and button.text == 'up':
							button.parent.increment = True
						if button.isOver(event.pos) and button.text == 'down':
							button.parent.decrement = True
				if event.type == pg.MOUSEBUTTONUP:
					for button in bt.Button.All:
						button.parent.increment = False
						button.parent.decrement = False

		pygame.quit()

def StartMainThread():
	print("Started running pygame")
	Main().main()
	print("Game closed")
	

def StartSerialThread():
	for i in range(0, 10):
		print("I'm just doing my own thing, whatever")
		time.sleep(1)
	print("finished")



if __name__ == "__main__":
	print("Started running program")
	print("Initialize serial queue")
	serialq = queue.Queue()
	print("Create Mainthread")
	MainThread = threading.Thread(target = StartMainThread)
	print("Create SerialThread")
	SerialThread = threading.Thread(target = StartSerialThread)
	MainThread.daemon = False
	SerialThread.deamon = False
	print("starting Application")
	SerialThread.start()
	MainThread.start()

# if __name__ == "__main__":
# 	print("Started running pygame")
# 	Main().main()
# 	print("Game closed")
