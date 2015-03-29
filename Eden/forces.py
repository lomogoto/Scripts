import c
import math

def gravitational(particle):
	return (0, -1 * c.gravitational * particle.mass)

def electric(particle1, particle2):
	magnitude = c.electric*particle1.charge*particle2.charge/get_distance(particle1.position, particle2.position)
	angle = get_angle(particle1.position, particle2.position)
	return [magnitude*angle[0], magnitude*angle[1]]

def magnetic(particle1, particle2):
	magnitude = 0	###
	return [0,0]		###

def strong(particle1, particle2):
	magnitude = c.strong*particle1.color*particle2.color/get_distance(particle1.position, particle2.position)
	angle = get_angle(particle1.position, particle2.position)
	return [magnitude*angle[0], magnitude*angle[1]]

def get_distance(position1, position2):
	d = ((position1[0]-position2[0])**2+(position1[1]-position2[1])**2)**.5
	if d==0:
		d=c.zero
	return d

def get_angle(position1,position2):
	distance = get_distance(position1, position2)
	return ((position1[0]-position2[0])/distance,(position1[1]-position2[1])/distance)
