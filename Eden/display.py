import pygame
import g
import c
import f
import particle
import math

pygame.init()
screen = pygame.display.set_mode((c.window_width,c.window_height))

move_position=(0,0)

def move():
	pygame.event.clear()
	pos1=pos2=None
	while pos1==None:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos1=event.pos
	while pos2==None:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos2=event.pos
	global move_position
	move_position=(move_position[0]+pos1[0]-pos2[0], move_position[1]+pos1[1]-pos2[1])

def update():
	screen.fill((20,20,20))
	screen.fill((10,10,10),((-move_position[0],-move_position[1]),(c.world_width,c.world_height)))
	for particle in g.particles:
		screen.fill(particle.get_color(), ((particle.position[0]-move_position[0],c.world_height-particle.position[1]-move_position[1]), (1,1)))
	pygame.display.update()

def add_electron():
	pygame.event.clear()
	pos1=pos2=None
	while pos1==None:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos1=event.pos
	while pos2==None:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos2=event.pos
	g.particles.append(particle.particle((pos1[0]+move_position[0],c.world_height-pos1[1]-move_position[1]), c.me, -1, False, (c.e_velocity, -f.get_angle(pos1, pos2)-math.pi)))

def add_proton():
	pygame.event.clear()
	pos=None
	while pos==None:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos=event.pos
	g.particles.append(particle.particle((pos[0]+move_position[0],c.world_height-pos[1]-move_position[1]), c.mp, 1, True))

def add_neutron():
	pygame.event.clear()
	pos=None
	while pos==None:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos=event.pos
	g.particles.append(particle.particle((pos[0]+move_position[0],c.world_height-pos[1]-move_position[1]), c.mn, 0, True))
