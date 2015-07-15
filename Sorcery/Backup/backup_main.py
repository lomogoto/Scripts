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

gamex, gamey = (320,256)
fullx, fully = (fullscreen.get_width(), fullscreen.get_height())

screen = pygame.Surface((gamex,gamey))

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for js in joysticks:
	js.init()

pygame.mouse.set_visible(0)

def get_scaling():
	if fullx/gamex > fully/gamey:
		return fully/gamey
	else:
		return fullx/gamex
	
def update():
	fullscreen.blit(pygame.transform.scale(screen, (gamex*get_scaling(), gamey*get_scaling())),(0,0))
	pygame.display.update()

def color_select():
	mapping=[None,None,None,None]
	img=pygame.image.load('Images/Player.png').convert()
	img.set_colorkey((0,0,0))
	while 1:
		screen.blit(pygame.image.load('Images/ColorSelect.png'),(0,0))
		for i in mapping:
			if i!=None:
				if i==0:
					screen.fill((0,150,0),((140,180),(30,30)))
					screen.blit(img,(145,186))
				elif i==1:
					screen.fill((150,0,0),((215,125),(30,30)))
					screen.blit(pygame.transform.rotate(img,90),(218,131))
				elif i==2:
					screen.fill((0,0,150),((50,110),(30,30)))
					screen.blit(pygame.transform.rotate(img,270),(52,113))
				elif i==3:
					screen.fill((75,0,75),((160,40),(27,27)))
					screen.blit(pygame.transform.rotate(img,180),(162,42))
		update()
		e=pygame.event.pump()		

		for js in joysticks:

			if js.get_button(Back_btn):
				if mapping==[None,None,None,None]:
					exit()
				else:
					mapping=[None,None,None,None]
			elif js.get_button(Start_btn):
				final_mapping=[]
				for i in range(4):
					if mapping[i]!=None:
						final_mapping.append([i,mapping[i]])
				return final_mapping
			elif js.get_button(A_btn):
				mapping[js.get_id()]=0
			elif js.get_button(B_btn):
				mapping[js.get_id()]=1
			elif js.get_button(X_btn):
				mapping[js.get_id()]=2
			elif js.get_button(Y_btn):
				mapping[js.get_id()]=3
		check_esc()

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

running=True

clock=pygame.time.Clock()

room_image=pygame.image.load('Images/Room.png')

while running:
	global_vars.reset()

	player_mapping = color_select()

	player_list=[]
	for p in player_mapping:
		player_list.append(player.Player(p[1],joysticks[p[0]]))
	
	players=pygame.sprite.Group(player_list)
	for p in player_list:
		global_vars.add_player(p)

	room=24
	alive=True
	doors, staircase = make_floor(room)
	while alive:
		screen.blit(room_image,(0,0))
		alive=False
		for p in global_vars.get_players():
			if p.health>0:
				alive=True

		global_vars.get_players().update()
		global_vars.get_hitboxes().update()
		global_vars.get_hitboxes().draw(screen)
		global_vars.get_players().draw(screen)	

		check_esc()		
		pygame.event.pump()
		clock.tick(60)
		update()
