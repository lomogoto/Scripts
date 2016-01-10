import organism
import heart
import orb
from random import randint

class Pot(organism.Organism):
	def __init__(self, pos):
		super(Pot,self).__init__()

		self.base_image=super(Pot,self).init_image('Images/pot.png')
		self.rect=self.base_image.get_rect().move(pos)

		self.health=1
		self.shot_strength=0
		self.speed=0
		self.drop_items=[heart.Heart, orb.Orb]
	
	def move(self):
		pass
