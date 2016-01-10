#!/usr/bin/env python2

import pygame
from random import randint
import global_vars
import player
import slime
import pot

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
imgRoom=pygame.image.load('Images/room.png').convert()

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

	global_vars.make_floor()

	global_vars.add_monster(slime.Slime((40,40)))
	global_vars.add_monster(pot.Pot((30,30)))

	running=1
	while running:
		check_esc()
		screen.fill((0,0,0))
		screen.blit(imgRoom,(0,0))
		screen.blit(global_vars.get_current_room().image, (8,8))
		doors=global_vars.get_current_room().doors
		if not doors[3]:
			screen.fill((0,0,0),((0,0),(8,88)))
		if not doors[0]:
			screen.fill((0,0,0),((0,0),(160,8)))
		if not doors[2]:
			screen.fill((0,0,0),((0,72),(160,16)))
		if not doors[1]:
			screen.fill((0,0,0),((152,0),(8,88)))
		global_vars.get_players().update()
		global_vars.get_monsters().update()
		global_vars.get_hitboxes().update()
		global_vars.get_items().update()
		global_vars.get_hitboxes().draw(screen)
		global_vars.get_monsters().draw(screen)
		global_vars.get_players().draw(screen)
		global_vars.get_items().draw(screen)
		for r in global_vars.get_rooms():
			if r.entered:
				color=(204,204,204)
				if global_vars.get_current_room().number==r.number:
					color=(204,0,204)
				screen.fill(color, ((152+r.number%8,80+r.number/8),(1,1)))

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
			
			for i in pygame.sprite.spritecollide(p, global_vars.get_items(), True):
				i.act(p)
			
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
				m.knock(boxes[0].direction+180)
			if m.health<1:
				m.kill()

		for p in global_vars.get_players():
			screen.blit(imgHeart,(40*p.special_num,80))
			screen.blit(imgNum[p.health],(40*p.special_num+8,80))
			screen.blit(imgOrb,(40*p.special_num+16,80))
			screen.blit(imgNum[p.orbs],(40*p.special_num+24,80))
			
		global_vars.move_room(global_vars.get_current_room().at_door(global_vars.players))
			
			
		pygame.event.pump()
		clock.tick(30)
		update()

while 1:
	check_esc()
	global_vars.reset()
	init_game()
