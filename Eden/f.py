import math
import c

def get_distance(position1, position2):
	distance = ((position1[0]-position2[0])**2+(position1[1]-position2[1])**2)**.5
	if distance==0:
		distance=c.zero
	return c.distance*distance

def get_angle(position1, position2):
	return math.atan2(position1[1]-position2[1],position1[0]-position2[0])

def vector_add(vector1, vector2):
	if not vector1[0]:
		return vector2
	elif not vector2[0]:
		return vector1
	magnitude = (vector1[0]**2+vector2[0]**2+2*vector1[0]*vector2[0]*math.cos(vector1[1]-vector2[1]))**.5
	if magnitude==0:
		return (0,0)
	try:
		return (magnitude, vector1[1]-math.asin(math.sin(vector1[1]-vector2[1])/magnitude*vector2[0]))
	except:
		print(magnitude, vector1, vector2)
		exit()
