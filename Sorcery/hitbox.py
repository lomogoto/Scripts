import pygame

class Hitbox(pygame.sprite.Sprite):
	def __init__(self, image, speed, time, poison, strength, stun, direction, pos):
		super(Hitbox, self).__init__()
		self.image=pygame.transform.rotate(image, direction-90)
		self.rect=image.get_rect(center=pos)
		self.strength=strength
		self.stun=stun
		self.direction=direction
		self.poison=poison
		self.speed=speed
		self.time=time

	def update(self):
		if self.time==0:
			self.kill()
		else:
			if self.direction==0:
				self.rect=self.rect.move(self.speed,0)
			elif self.direction==180:
				self.rect=self.rect.move(-self.speed,0)
			elif self.direction==90:
				self.rect=self.rect.move(0,-self.speed)
			elif self.direction==270:
				self.rect=self.rect.move(0,self.speed)
			self.time-=1
