import pygame
import g
import c

pygame.init()
screen = pygame.display.set_mode((c.window_width,c.window_height))


def update():
	screen.fill((0,0,0))
	for particle in g.particles:
		screen.fill(particle.get_color(), (particle.position, (1,1)))
	pygame.display.update()
