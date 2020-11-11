"""Defines the button class"""
import pygame

class Button():

	All = []

	def __init__(self, color, x, y, width, height, parent_object , text=' '):
		self.color    = color
		self.x        = x
		self.xmid     = x + width  / 2
		self.ymid     = y + height / 2
		self.y        = y
		self.width    = width
		self.height   = height
		self.text     = text
		self.font     = pygame.font.SysFont('Ubuntu', 22)
		self.All.append(self)
		self.parent   = parent_object

	def draw(self,win,outline=None):
		#Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
		pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

		"""Draw triangle buttons"""
		if self.text == 'down':
			pygame.draw.polygon(win, (0, 0, 0), [(self.xmid-self.width/2,self.y+7),(self.xmid,self.ymid+self.height/4+7),(self.xmid+self.width/2,self.y+7)])
		elif self.text == 'up':
			pygame.draw.polygon(win, (0, 0, 0), [(self.xmid-self.width/2,self.y+self.height),(self.xmid,self.ymid-self.height/4),(self.xmid+self.width/2,self.y+self.height)])
		else:
			text = self.font.render(self.text, 1, (0,0,0))
			win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

	def isOver(self, pos):
		#Pos is the mouse position or a tuple of (x,y) coordinates
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True
		return False


if __name__ == "__main__":
	print("Started running in button.py")
	execfile('Main.py')		