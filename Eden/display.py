import pygame
import g
import c
import f
import particle

pygame.init()
screen = pygame.display.set_mode((c.window_width,c.window_height))


def update():
	screen.fill((10,10,10))
	for particle in g.particles:
		screen.fill(particle.get_color(), (particle.position, (1,1)))
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
	g.particles.append(particle.particle(pos1, c.me, -1, False, (c.e_velocity, f.get_angle(pos1, pos2))))

def add_proton():
	pygame.event.clear()
	pos=None
	while pos==None:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos=event.pos
	g.particles.append(particle.particle(pos, c.mp, 1, True))

def add_neutron():
	pygame.event.clear()
	pos=None
	while pos==None:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos=event.pos
	g.particles.append(particle.particle(pos, c.mn, 0, True))
