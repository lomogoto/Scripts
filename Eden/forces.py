import c
import f
import math

def gravitational(particle):
	return (c.gravitational*particle.mass, math.pi*1.5)

def electric(particle1, particle2):
	Fe=(c.electric*c.e**2*particle1.charge*particle2.charge/f.get_distance(particle1.position, particle2.position), f.get_angle(particle1.position, particle2.position))
	if particle1.spin*particle2.spin<0:
		return (Fe[0]*c.magnetic,Fe[1])
	elif particle1.spin*particle2.spin>0:
		if f.get_distance(particle1.position, particle2.position)>c.spin_switch_distance:
			return (Fe[0]*(2-c.magnetic),Fe[1])
		else:
			particle1.spin*=-1
			return (0,0)
	return Fe
	
def strong(particle1, particle2):
	distance=f.get_distance(particle1.position, particle2.position)
	if distance>c.strong_range[0] and distance<c.strong_range[1]:
		return (c.strong*particle1.color*particle2.color, f.get_angle(particle1.position, particle2.position)+math.pi)
	else:
		return (0,0)
