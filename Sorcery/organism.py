import pygame
import random
import global_vars
import hitbox

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
		self.attacking=0
		self.orientation=0

	def init_image(self, path):
		img=pygame.image.load(path).convert()
		img.set_colorkey((255,255,255))
		return img

	def update_image(self):
		self.image=pygame.transform.rotate(self.base_image, self.orientation)
	
	def knock(self, orientation=None):
		if orientation!=None:
			self.orientation=orientation
		if self.health<1:
			return
		if self.orientation==0:
			self.rect=self.rect.move(0,8)
		elif self.orientation==90:
			self.rect=self.rect.move(8,0)
		elif self.orientation==180:
			self.rect=self.rect.move(0,-8)
		else:
			self.rect=self.rect.move(-8,0)

	def move(self):
		pass

	def follow(self):
		pos=self.get_closest()
		[x,y]=self.rect.center
		move=[0,0]
		if x!=pos[0]:
			move=[self.speed*(pos[0]-x)/abs(pos[0]-x)*random.randint(0,1),0]
		if move==[0,0]:
			if pos[1]==y:
				move=[self.speed*(pos[0]-x)/abs(pos[0]-x),0]
			else:
				move=[0,self.speed*(pos[1]-y)/abs(pos[1]-y)]
		if move[1]<0:
			self.orientation=0
		elif move[0]<0:
			self.orientation=90
		elif move[1]>0:
			self.orientation=180
		elif move[0]>0:
			self.orientation=270
		self.rect=self.rect.move(move[0],move[1])

	def hide(self):
		pass
	def aim(self):
		pass
	def attack(self):
		pass

	def shoot(self, image=None, d=None, strength=None, speed=None, stun=None, poison=None, time=60):
		
		if image==None:
			image=self.shot_image
			d=6
			strength=self.shot_strength
			speed=self.shot_speed
			stun=self.shot_stun
			poison=self.shot_poison

		pos=self.rect.center
		if self.orientation==0:
			pos=(pos[0],pos[1]-d)
		elif self.orientation==90:
			pos=(pos[0]-d, pos[1])
		elif self.orientation==180:
			pos=(pos[0], pos[1]+d)
		elif self.orientation==270:
			pos=(pos[0]+d, pos[1])
		self.attacking=10
		global_vars.add_hitbox(hitbox.Hitbox(image, pos, self.orientation, strength, speed, stun, poison, time))

	def get_closest(self):
		closest=None
		for p in global_vars.get_players():
			if (closest==None or self.distance(p)<self.distance(closest)) and p.health>0:
				closest=p
		return closest.rect.center
	
	def distance(self, p):
		return ((self.rect.center[0]-p.rect.center[0])**2+(self.rect.center[1]-p.rect.center[1])**2)**.5

	def update(self):
		self.clock+=1
		if self.stun==0:
			self.move()
			if not self.attacking and self.health>0:
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
		self.rect=self.rect.clamp(pygame.Rect(8,8,144,64))
