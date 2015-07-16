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
	for js in joysticks:
		js.init()
	
	playing_joysticks=[]
	
	connecting=1
	while connecting:
		check_esc()
		for js in joysticks:
			if js.get_button(0):
				playing_joysticks.append(js)
			if js.get_button(7) and len(playing_joysticks)>0:
				connecting=0
			if js.get_button(6):
				playing_joysticks=[]
		playing_joysticks=list(set(playing_joysticks))
		screen.fill((0,0,0))
		if len(playing_joysticks)==0:
			screen.blit(pygame.image.load('Images/0.png').convert(),(76,40))
		elif len(playing_joysticks)==1:
			screen.blit(pygame.image.load('Images/1.png').convert(),(76,40))
		elif len(playing_joysticks)==2:
			screen.blit(pygame.image.load('Images/2.png').convert(),(76,40))
		elif len(playing_joysticks)==3:
			screen.blit(pygame.image.load('Images/3.png').convert(),(76,40))
		else:
			screen.blit(pygame.image.load('Images/4.png').convert(),(76,40))
		pygame.event.pump()
		clock.tick(30)
		update()
	i=0
	for js in playing_joysticks[0:4]:
		global_vars.add_player(player.Player(i, js))
		i+=1

	running=1
	while running:
		check_esc()
		screen.fill((0,0,0))
		global_vars.get_players().update()
		global_vars.get_hitboxes().update()
		global_vars.get_hitboxes().draw(screen)
		global_vars.get_players().draw(screen)	

		running=0
		for p in global_vars.get_players():
			boxes=pygame.sprite.spritecollide(p, global_vars.get_hitboxes(), True)
			for box in boxes:
				p.health-=box.strength
				p.stun=box.stun
				p.poison=box.poison
			monsters=pygame.sprite.spritecollide(p, global_vars.get_monsters(), False)
			for m in monsters:
				p.health-=m.strength
				p.stun=m.stun
				p.poison=m.poison
			if len(boxes)>0 or len(monsters)>0:
				d=p.orientation
				if d==0:
					p.rect=p.rect.move(0,8)
				elif d==90:
					p.rect=p.rect.move(8,0)
				elif d==180:
					p.rect=p.rect.move(0,-8)
				else:
					p.rect=p.rect.move(-8,0)
			if p.health>0:
				running=1
		for m in global_vars.get_monsters():
			boxes=pygame.sprite.spritecollide(m, global_vars.get_hitboxes(), True)
			for box in boxes:
				m.health-=box.strength
				m.stun=box.stun
				m.poison=box.poison

		pygame.event.pump()
		clock.tick(30)
		update()

while 1:
	check_esc()
	global_vars.reset()
	init_game()
