import pygame
import copy
import room
from random import randint

monsters=pygame.sprite.Group()
players=pygame.sprite.Group()
hitboxes=pygame.sprite.Group()
items=pygame.sprite.Group()
rooms=[]
current_room_num=randint(0,63)
screen=None
level=0

def get_rooms():
	return rooms

def get_current_room():
	return rooms[current_room_num]

def move_room(direction):
	global hitboxes
	global monsters
	global items
	if direction==-1:
		make_floor()
		hitboxes.empty()
		monsters.empty()
		items.empty()
	elif get_current_room().get_next_room_number(direction)!=None:
		get_current_room().entered=True
		global current_room_num
		current_room_num=get_current_room().get_next_room_number(direction)
		get_current_room().entered=True
		hitboxes.empty()
		monsters.empty()
		items.empty()
		add_monsters()

		for p in players:
			if direction==0:
				p.rect.center=(80,64)
			elif direction==3:
				p.rect.center=(144,40)
			elif direction==2:
				p.rect.center=(80,16)
			elif direction==1:
				p.rect.center=(16,40)

def add_monsters():
	pass

def add_item(i):
	global items
	items.add(i)

def get_items():
	return items

def make_floor():
	global level
	level+=1
	global rooms
	rooms=[]
	for i in range(64):
		rooms.append(room.Room(i))
	r1=copy.copy(get_current_room())
	for i in xrange(randint(15,20)):
		direction=randint(0,3)
		num=r1.get_next_room_number(direction)
		if not num==None:
			r2=rooms[num]
			r1.doors[direction]=1
			r2.doors[direction-2]=1
			r1=copy.copy(r2)
	r2.end=True
	get_current_room().entered=True

	for i in xrange(randint(30,60)):
		r=rooms[randint(0,63)]
		d=randint(0,3)
		if r.get_next_room_number(d)!=None:
			rooms[r.get_next_room_number(d)].doors[d-2]=1
			r.doors[d]=1

	for r in rooms:
		r.generate_image()

def get_screen():
	return screen

def add_monster(m):
	global monsters
	monsters.add(m)

def get_monsters():
	return monsters

def add_player(p):
	global players
	players.add(p)

def get_players():
	return players

def add_hitbox(h):
	global hitboxes
	hitboxes.add(h)

def get_hitboxes():
	return hitboxes

def reset():
	global monsters
	monsters.empty()
	global players
	players.empty()
	global hitboxes
	hitboxes.empty()
	global rooms
	rooms=[]
	global current_room_num
	current_room_num=randint(0,63)
	global level
	level=0
	global items
	items.empty()
