#!/usr/bin/env python2

import pygame

pygame.init()
screen=pygame.display.set_mode((50,50))
screen.fill((255,255,255))

joystick = pygame.joystick.Joystick(0)
joystick.init()

while 1:
	for e in pygame.event.get():
		if e.type == pygame.KEYDOWN:
			exit()
		elif e.type == pygame.JOYBUTTONDOWN:
			print e.button
		elif e.type == pygame.JOYAXISMOTION:
			print e.axis
			print e.pos
