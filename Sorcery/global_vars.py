import pygame

monsters=pygame.sprite.Group()
players=pygame.sprite.Group()
hitboxes=pygame.sprite.Group()

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
