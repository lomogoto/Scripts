from random import randint
import pygame

class Room():
	def __init__(self, number):
		self.number=number
		self.end=False
		self.doors=[0,0,0,0]
		self.entered=False
		self.locked=False

	def generate_image(self):
		img=pygame.Surface((36,16))
		img.fill((102,51,0))
		for i in xrange(150):
			img.fill((153,102,51),((randint(0,35),randint(0,15)),(1,1)))
		for i in xrange(150):
			img.fill((153,51,0),((randint(0,35),randint(0,15)),(1,1)))

		if self.end:
			img.fill((0,0,0),((16,5),(4,6)))
			img.fill((0,0,0),((15,6),(6,4)))

		self.image=pygame.transform.scale(img, (144,64))

	def get_next_room_number(self, direction):
		if direction==0 and self.number>7:
			return self.number-8
		elif direction==1 and (self.number+1)%8>0:
			return self.number+1
		elif direction==3 and (self.number)%8>0:
			return self.number-1
		elif direction==2 and self.number<56:
			return self.number+8
		else:
			return None
	def at_door(self, group):
		door=pygame.sprite.Sprite()
		door.rect=pygame.Rect((79,8),(2,1))
		if pygame.sprite.spritecollide(door, group, False) and self.doors[0]:
			print self.number
			return 0
		door.rect=pygame.Rect((79,71),(2,1))
		if pygame.sprite.spritecollide(door, group, False) and self.doors[2]:
			print self.number
			return 2
		door.rect=pygame.Rect((8,39),(1,2))
		if pygame.sprite.spritecollide(door, group, False) and self.doors[3]:
			print self.number
			return 3
		door.rect=pygame.Rect((151,39),(1,2))
		if pygame.sprite.spritecollide(door, group, False) and self.doors[1]:
			print self.number
			return 1
		door.rect=pygame.Rect((70,30),(20,20))
		if self.end and pygame.sprite.spritecollide(door, group, False):
			return -1
