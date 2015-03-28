import pygame
import random

class Organism(pygame.sprite.Sprite):
	def __init__(self):
		super(Organism, self).__init__()
		self.health=0
		self.poison=0
		self.stun=0
		self.melee_strength=0
		self.melee_poison=0
		self.melee_stun=0
		self.blast_strength=0
		self.blast_stun=0
		self.blast_poison=0
		self.blast_speed=1
		self.drop_items=[]
		self.clock=0
