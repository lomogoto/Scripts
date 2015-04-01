import c
import f
import math

def gravitational(particle):
	return (c.gravitational*particle.mass, math.pi*1.5)

def electric(particle1, particle2):
	return (c.electric*c.e**2*particle1.charge*particle2.charge/f.get_distance(particle1.position, particle2.position), f.get_angle(particle1.position, particle2.position))

def magnetic(particle1, particle2):
	return (c.magnetic*particle1.spin*particle2.spin/f.get_distance(particle1.position, particle2.position), f.get_angle(particle1.position, particle2.position))

def strong(particle1, particle2):
	distance=f.get_distance(particle1.position, particle2.position)
	if distance>c.strong_range[0] and distance<c.strong_range[1]:
		return (c.strong*particle1.color*particle2.color, f.get_angle(particle1.position, particle2.position)+math.pi)
	else:
		return (0,0)
