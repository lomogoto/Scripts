import organism
import pygame

class Slime(organism.Organism):
	def __init__(self):
		super(Slime,self).__init__()

		self.base_image=super(Slime,self).init_image('Images/slime.png')
		self.rect=self.base_image.get_rect().move(20,20)
		self.health=2
		self.shot_strength=1
		self.shot_stun=10
		self.speed=4
	
	def move(self):
		if self.clock%30<2:
			super(Slime,self).follow()
