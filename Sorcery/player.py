import organism
import global_vars

class Player(organism.Organism):
	def __init__(self, character_num, joystick):
		super(Player,self).__init__()

		self.base_image=super(Player,self).init_image('Images/P'+str(character_num+1)+'.png')
		self.shot_image=super(Player,self).init_image('Images/P'+str(character_num+1)+'_shot.png')
		self.ghost_image=super(Player,self).init_image('Images/P'+str(character_num+1)+'_ghost.png')
		self.special_image=super(Player,self).init_image('Images/P'+str(character_num+1)+'_special.png')

		self.shot_strength=1
		self.shot_speed=1
		self.shot_stun=0
		self.shot_poison=0

		self.image=self.base_image

		self.health=3
		self.orbs=3

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

		if self.joystick.get_button(9)==True:
			self.health=0

	def special(self):
		if self.special_num==0:
			pass
		elif self.special_num==1:
			super(Player,self).shoot(self.special_image, 10, -3, 0, 0, 0, 10)
		elif self.special_num==2:
			global_vars.get_screen().blit(self.special_image, (0,0))
			for m in global_vars.get_monsters():
				m.stun+=90
		elif self.special_num==3:
			global_vars.get_screen().blit(self.special_image, (0,0))
			for m in global_vars.get_monsters():
				m.poison+=10

	def attack(self):
		xAxis=self.joystick.get_axis(3)
		yAxis=self.joystick.get_axis(4)
		a=0
		if yAxis<-.75:
			a=1
			self.orientation=0
		elif xAxis<-.75:
			a=1
			self.orientation=90
		elif yAxis>.75:
			a=1
			self.orientation=180
		elif xAxis>.75:
			a=1
			self.orientation=270

		if a:
			super(Player,self).shoot()
		
		if self.orbs>0:
			self.orbs-=1
			self.attacking+=10
			if self.joystick.get_axis(5)>.25:
				self.special()
			elif self.joystick.get_button(0):
				self.shot_speed+=1
			elif self.joystick.get_button(1):
				self.shot_strength+=1
			elif self.joystick.get_button(2):
				self.shot_stun+=1
			elif self.joystick.get_button(3):
				self.shot_poison+=1
			else:
				self.orbs+=1
				self.attacking-=10

	def update_image(self):
		super(Player, self).update_image()
		if self.health<1:
			self.image=self.ghost_image
