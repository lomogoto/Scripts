#!/usr/bin/env python2

import pygame
from random import randint
import global_vars
import player

A_btn=0
B_btn=1
X_btn=2
Y_btn=3

Start_btn=7
Back_btn=6

pygame.init()
fullscreen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

gamex, gamey = (160,88)
fullx, fully = (fullscreen.get_width(), fullscreen.get_height())

screen = pygame.Surface((gamex,gamey))

pygame.mouse.set_visible(0)

clock=pygame.time.Clock()

def get_scaling():
	if fullx/gamex > fully/gamey:
		return fully/gamey
	else:
		return fullx/gamex
	
def update():
	fullscreen.blit(pygame.transform.scale(screen, (gamex*get_scaling(), gamey*get_scaling())),(0,0))
	pygame.display.update()

def check_esc():
	if pygame.key.get_pressed()[pygame.K_ESCAPE]:
		exit()

def make_floor(starting_room):
	doors=[]
	for i in xrange(84):
		doors.append(0)
	room=starting_room
	for i in range(randint(5,10)):
		direction=randint(0,3)
		if direction==0 and room-7<0:
			doors[room+room/7*6-7]=1
			room-=7
		elif direction==3 and room%7!=0:
			doors[room+room/7*6-1]=1
			room-=1
		elif direction==1 and room%7!=6:
			doors[room+room/7*6]=1
			room+=1
		elif direction==2 and room+7>48:
			doors[room+room/7*6+6]=1
			room+=6
	for i in range(randint(40,60)):
		doors[randint(0,83)]=1
	return [doors,room]

def init_game():
	joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
	i=0
	for js in joysticks:
		js.init()
		global_vars.add_player(player.Player(i,js))
		i+=1
	
	running=1
	while running:
		global_vars.get_players().update()
		global_vars.get_hitboxes().update()
		global_vars.get_hitboxes().draw(screen)
		global_vars.get_players().draw(screen)	

		check_esc()		
		pygame.event.pump()
		clock.tick(30)
		update()

init_game()
