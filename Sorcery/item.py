import pygame

class Item(pygame.sprite.Sprite):
	def __init__(self):
		super(Item,self).__init__()
	
	def init_image(self, path):
		img=pygame.image.load(path).convert()
		img.set_colorkey((255,255,255))
		return img
	
	def act(self, player):
		pass
	
	def update(self):
		pass
