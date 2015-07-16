#!/usr/bin/env python2

import pygame
from random import randint
import global_vars
import player
import slime

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

global_vars.screen=screen

pygame.mouse.set_visible(0)

clock=pygame.time.Clock()

imgNum=[
pygame.image.load('Images/0.png').convert(),
pygame.image.load('Images/1.png').convert(),
pygame.image.load('Images/2.png').convert(),
pygame.image.load('Images/3.png').convert(),
pygame.image.load('Images/4.png').convert(),
pygame.image.load('Images/5.png').convert(),
pygame.image.load('Images/6.png').convert(),
pygame.image.load('Images/7.png').convert(),
pygame.image.load('Images/8.png').convert(),
pygame.image.load('Images/9.png').convert() ]

imgHeart=pygame.image.load('Images/heart.png').convert()
imgHeart.set_colorkey((255,255,255))
imgOrb=pygame.image.load('Images/orb.png').convert()
imgOrb.set_colorkey((255,255,255))

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
			screen.blit(imgNum[0],(76,40))
		elif len(playing_joysticks)==1:
			screen.blit(imgNum[1],(76,40))
		elif len(playing_joysticks)==2:
			screen.blit(imgNum[2],(76,40))
		elif len(playing_joysticks)==3:
			screen.blit(imgNum[3],(76,40))
		else:
			screen.blit(imgNum[4],(76,40))
		pygame.event.pump()
		clock.tick(30)
		update()
	i=0
	for js in playing_joysticks[0:4]:
		global_vars.add_player(player.Player(i, js))
		i+=1

	global_vars.add_monster(slime.Slime())

	running=1
	while running:
		check_esc()
		screen.fill((0,0,255))
		screen.fill((102,102,102),((8,8),(144,64)))
		global_vars.get_players().update()
		global_vars.get_monsters().update()
		global_vars.get_hitboxes().update()
		global_vars.get_hitboxes().draw(screen)
		global_vars.get_monsters().draw(screen)
		global_vars.get_players().draw(screen)
		screen.fill((0,0,0),((0,0),(8,88)))
		screen.fill((0,0,0),((0,0),(160,8)))
		screen.fill((0,0,0),((0,72),(160,16)))
		screen.fill((0,0,0),((152,0),(8,88)))

		running=0
		for p in global_vars.get_players():
			boxes=pygame.sprite.spritecollide(p, global_vars.get_hitboxes(), True)
			for box in boxes:
				p.health-=box.strength
				p.stun=box.stun
				p.poison=box.poison
			monsters=pygame.sprite.spritecollide(p, global_vars.get_monsters(), False)
			for m in monsters:
				p.health-=m.shot_strength
				p.stun=m.shot_stun
				p.poison=m.shot_poison
			if len(boxes)>0 or len(monsters)>0:
				p.knock()
			if p.health>0:
				running=1
			else:
				p.health=0
		for m in global_vars.get_monsters():
			boxes=pygame.sprite.spritecollide(m, global_vars.get_hitboxes(), True)
			for box in boxes:
				m.health-=box.strength
				m.stun=box.stun
				m.poison=box.poison
			if len(boxes)>0:
				m.knock()
			if m.health<1:
				m.kill()

		for p in global_vars.get_players():
			screen.blit(imgHeart,(40*p.special_num,80))
			screen.blit(imgNum[p.health],(40*p.special_num+8,80))
			screen.blit(imgOrb,(40*p.special_num+16,80))
			screen.blit(imgNum[p.orbs],(40*p.special_num+24,80))
			
		
		pygame.event.pump()
		clock.tick(30)
		update()

while 1:
	check_esc()
	global_vars.reset()
	init_game()
