import organism
import pygame
import copy
import hitbox
import global_vars

class Player(organism.Organism):
	def __init__(self, character_num, joystick):
		super(Player,self).__init__()

		if character_num==0:
			self.image=pygame.image.load('Images/P1.png').convert()
		elif character_num==1:
			self.image=pygame.image.load('Images/P2.png').convert()
		elif character_num==2:
			self.image=pygame.image.load('Images/P3.png').convert()
		else:
			self.image=pygame.image.load('Images/P4.png').convert()
		
		
		self.image.set_colorkey((0,0,0))

	
		self.health=9
		self.special_num=character_num
		self.joystick=joystick
		self.joystick.init()
		self.rect=self.image.get_rect()
		self.orientation=0
		self.attacking=0

	def move(self):
		xAxis=self.joystick.get_axis(0)
		yAxis=self.joystick.get_axis(1)
		fast=self.health>1 and not self.attacking
		if xAxis<-.25:
			self.rect=self.rect.move(-1-fast,0)
		elif xAxis>.25:
			self.rect=self.rect.move(1+fast,0)
		if yAxis<-.25:
			self.rect=self.rect.move(0,-1-fast)
		elif yAxis>.25:
			self.rect=self.rect.move(0,1+fast)
		self.rect=self.rect.clamp(pygame.Rect(8,8,80,180))

	def attack(self):
		if self.health>0:
			if self.joystick.get_button(0):
				self.attacking=15
				
				pos=self.rect.center

				if self.orientation==0:
					pos=(pos[0]+26,pos[1]-8)
				elif self.orientation==90:
					pos=(pos[0],pos[1]-19)
				elif self.orientation==180:
					pos=(pos[0]-11,pos[1]-8)
				else:
					pos=(pos[0],pos[1]+19)

				global_vars.add_hitbox()

	def update(self):
		if self.joystick.get_button(9)==True:
			self.health=0
		if self.stun==0:
			self.move()
			if not self.attacking:
				self.attack()
			else:
				self.attacking-=1
		else:
			self.stun-=1
		if self.poison and self.clock%60:
			self.health-=1
			self.poison-=1
		if self.health<0:
			self.health=0
