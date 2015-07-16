import pygame
import random

class Organism(pygame.sprite.Sprite):
	def __init__(self):
		super(Organism, self).__init__()
		self.health=0
		self.poison=0
		self.stun=0
		self.shot_strength=0
		self.shot_stun=0
		self.shot_poison=0
		self.shot_speed=0
		self.drop_items=[]
		self.clock=0
		self.speed=0

	def update_image(self):
		self.image=pygame.transform.rotate(self.base_image, self.orientation))

	def move(self):
		pass

	def follow(self):
		pos=get_closest()
		[x,y]=self.rect.center
		move=[0,0]
		if x!=pos[0]:
			move=[self.speed*(pos[0]-x)/abs(pos[0]-x)*random.randint(0,1),0]
		if move==[0,0]:
			move=[0,self.speed*(pos[1]-y)/abs(pos[1]-y)*random.randint(0,1)]

	def hide(self):
	
	def aim(self):

	def attack(self):
		pass

	def get_closest(self):
		closest=None
		for p in global_vars.get_players()
			if closest==None or distance(p)<distance(closest):
				closest=p
		return closest.rect.center
	
	def distance(self, p)
		return ((self.rect.center[0]-p.rect.center[0])**2+(self.rect.center[1]-p.rect.center[1])**2)**.5

	def update(self):
		if self.stun==0:
			self.move()
			if not self.attacking:
				self.attack()
			else:
				self.attacking-=1
		else:
			self.stun-=1
		if self.poison and self.clock%60==0:
			self.health-=(self.health!=1)
			self.poison-=1
		if self.health<0:
			self.health=0
		self.update_image()
