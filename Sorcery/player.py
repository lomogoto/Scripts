import organism
import pygame
import copy
import hitbox
import global_vars

class Player(organism.Organism):
	def __init__(self, character_num, joystick):
		super(Player,self).__init__()

		self.base_image=pygame.image.load('Images/Player.png').convert()
		self.base_image.set_colorkey((0,0,0))

		if character_num==0:
			staff=pygame.image.load('Images/Green.png').convert()
		elif character_num==1:
			staff=pygame.image.load('Images/Red.png').convert()
		elif character_num==2:
			staff=pygame.image.load('Images/Blue.png').convert()
		else:
			staff=pygame.image.load('Images/Purple.png').convert()

		staff.set_colorkey((0,0,0))

		self.hat_image=copy.copy(self.base_image)
		hat=pygame.image.load('Images/Hat.png').convert()
		hat.set_colorkey((0,0,0))
		self.hat_image.blit(hat,(0,1))

		self.rest_image=copy.copy(self.base_image)
		self.rest_image.blit(staff,(15,0))

		self.rest_hat_image=copy.copy(self.hat_image)
		self.rest_hat_image.blit(staff,(15,0))

		self.image=self.base_image

		self.melee_image=pygame.image.load('Images/Melee.png').convert()
		self.melee_image.set_colorkey((0,0,0))
		self.melee_image.blit(staff,(0,5))
	
		self.blast_image=pygame.image.load('Images/Blast.png').convert()
		self.blast_image.set_colorkey((0,0,0))
		self.blast_image.blit(staff, (4,1))

		self.health=3
		self.special_num=character_num
		self.joystick=joystick
		self.joystick.init()
		self.rect=self.image.get_rect()
		self.orientation=0
		self.attacking=0
		self.hat=character_num==0

	def update_img(self):
		if self.health>0:
			if self.attacking:
				if self.hat:
					self.image=pygame.transform.rotate(self.hat_image,self.orientation-90)
				else:
					self.image=pygame.transform.rotate(self.base_image,self.orientation-90)
			else:
				if self.hat:
					self.image=pygame.transform.rotate(self.rest_hat_image,self.orientation-90)
				else:
					self.image=pygame.transform.rotate(self.rest_image,self.orientation-90)
		else:
			pass
			
	def move(self):
		xAxis=self.joystick.get_axis(0)
		yAxis=self.joystick.get_axis(1)
		if xAxis<-.25:
			self.rect=self.rect.move(-1,0)
		elif xAxis>.25:
			self.rect=self.rect.move(1,0)
		if yAxis<-.25:
			self.rect=self.rect.move(0,-1)
		elif yAxis>.25:
			self.rect=self.rect.move(0,1)
		if self.health>1 and not self.attacking:
			if abs(xAxis)>abs(yAxis):
				if xAxis<-.75:
					self.rect=self.rect.move(-1,0)
					self.orientation=180
				elif xAxis>.75:
					self.rect=self.rect.move(1,0)
					self.orientation=0
			else:
				if yAxis<-.75:
					self.rect=self.rect.move(0,-1)
					self.orientation=90
				elif yAxis>.75:
					self.rect=self.rect.move(0,1)
					self.orientation=270
		self.rect=self.rect.clamp(pygame.Rect(32,32,256,192))

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

				global_vars.add_hitbox(hitbox.Hitbox(self.melee_image, 0, 5, self.melee_poison, self.melee_strength, self.melee_stun, self.orientation, pos))

			elif self.joystick.get_button(1):
				self.attacking=30

				global_vars.add_hitbox(hitbox.Hitbox(self.blast_image, self.blast_speed, 240, self.blast_poison, self.blast_strength, self.blast_stun, self.orientation, self.rect.center))

	def update(self):
		if self.joystick.get_button(9)==True:
			self.health=0
		if self.stun==0:
			self.move()
			if not self.attacking:
				self.attack()
			else:
				self.attacking-=1
		if self.poison and self.clock%60:
			self.health-=1
			self.poison-=1
		if self.health<0:
			self.health=0
		self.update_img()
