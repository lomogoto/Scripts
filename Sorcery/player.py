import organism
import pygame
import copy
import hitbox
import global_vars

class Player(organism.Organism):
	def __init__(self, character_num, joystick):
		super(Player,self).__init__()

		if character_num==0:
			self.base_image=pygame.image.load('Images/P1.png').convert()
			self.shot_image=pygame.image.load('Images/P1_shot.png').convert()
			self.special_image=pygame.image.load('Images/P1_special.png').convert()
			self.ghost_image=pygame.image.load('Images/P1_ghost.png').convert()
		elif character_num==1:
			self.base_image=pygame.image.load('Images/P2.png').convert()
			self.shot_image=pygame.image.load('Images/P2_shot.png').convert()
			self.special_image=pygame.image.load('Images/P2_special.png').convert()
			self.ghost_image=pygame.image.load('Images/P2_ghost.png').convert()
		elif character_num==2:
			self.base_image=pygame.image.load('Images/P3.png').convert()
			self.shot_image=pygame.image.load('Images/P3_shot.png').convert()
			self.special_image=pygame.image.load('Images/P3_special.png').convert()
			self.ghost_image=pygame.image.load('Images/P3_ghost.png').convert()
		else:
			self.base_image=pygame.image.load('Images/P4.png').convert()
			self.shot_image=pygame.image.load('Images/P4_shot.png').convert()
			self.special_image=pygame.image.load('Images/P4_special.png').convert()
			self.ghost_image=pygame.image.load('Images/P4_ghost.png').convert()
		
		self.base_image.set_colorkey((255,255,255))	
		self.shot_image.set_colorkey((255,255,255))	
		self.special_image.set_colorkey((255,255,255))	
		self.ghost_image.set_colorkey((255,255,255))

		self.shot_strength=1
		self.shot_speed=1
		self.shot_stun=0
		self.shot_poison=0

		self.image=self.base_image

		self.health=9
		self.special_num=character_num
		self.joystick=joystick
		self.joystick.init()
		self.rect=self.base_image.get_rect()
		self.orientation=0
		self.attacking=0

	def move(self):
		xAxis=self.joystick.get_axis(0)
		yAxis=self.joystick.get_axis(1)
		fast=self.health>1 and not self.attacking
		if xAxis<-.75:
			self.rect=self.rect.move(-1-fast,0)
			if not self.attacking:
				self.orientation=90
		elif xAxis>.75:
			self.rect=self.rect.move(1+fast,0)
			if not self.attacking:
				self.orientation=270
		elif yAxis<-.75:
			self.rect=self.rect.move(0,-1-fast)
			if not self.attacking:
				self.orientation=0
		elif yAxis>.75:
			self.rect=self.rect.move(0,1+fast)
			if not self.attacking:
				self.orientation=180
		self.rect=self.rect.clamp(pygame.Rect(8,8,152,80))

		if self.joystick.get_button(9)==True:
			self.health=0

	def attack(self):
		if self.health>0 and not self.attacking:
			pos=self.rect.center
			xAxis=self.joystick.get_axis(3)
			yAxis=self.joystick.get_axis(4)

			if yAxis<-.75:
				self.orientation=0
				pos=(pos[0],pos[1]-6)
			elif xAxis<-.75:
				self.orientation=90
				pos=(pos[0]-6,pos[1])
			elif yAxis>.75:
				self.orientation=180
				pos=(pos[0],pos[1]+6)
			elif xAxis>.75:
				self.orientation=270
				pos=(pos[0]+6,pos[1])

			if not pos==self.rect.center:
				self.attacking=10
				global_vars.add_hitbox(hitbox.Hitbox(self.shot_image, pos, self.orientation, self.shot_strength, self.shot_speed, self.shot_stun, self.shot_poison))

	def update_image(self):
		super(Player, self).update_image()
		self.image=self.ghost_image
