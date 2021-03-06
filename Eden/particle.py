import f
import c
import math

class particle():
	def __init__(self, position, mass, charge, color=False, spin=0, velocity=(0,0)):
		self.charge=charge
		self.color=color
		self.mass=mass
		self.position=position
		self.velocity=velocity
		self.spin=spin

		self.new_velocity=self.velocity

	def update(self):
		if self.new_velocity[0]>c.max_speed:
			self.new_velocity=(c.max_speed,self.new_velocity[1])
		self.velocity=self.new_velocity
		self.position=(self.position[0]+c.frame*self.velocity[0]*math.cos(self.velocity[1]), self.position[1]+c.frame*self.velocity[0]*math.sin(self.velocity[1]))
		if self.position[0]<0:
			self.position=(0, self.position[1])
			self.new_velocity=(abs(self.new_velocity[0]), 0)
		elif self.position[0]>c.world_width:
			self.position=(c.world_width, self.position[1])
			self.new_velocity=(abs(self.new_velocity[0]), math.pi)
		if self.position[1]<0:
			self.position=(self.position[0], 0)
			self.new_velocity=(abs(self.new_velocity[0]), .5*math.pi)
		elif self.position[1]>c.world_height:
			self.position=(self.position[0], c.world_height)
			self.new_velocity=(abs(self.new_velocity[0]), 1.5*math.pi)

	def apply_force(self, force):
		self.new_velocity=f.vector_add(self.new_velocity, (force[0]/self.mass*c.frame, force[1]))

		if self.new_velocity[0]<0:
			self.new_velocity=(self.new_velocity[0]*-1, self.new_velocity[1]+2*math.pi)
		while self.new_velocity[1]>=2*math.pi:
			self.new_velocity=(self.new_velocity[0], self.new_velocity[1]-2*math.pi)
		while self.new_velocity[1]<0:
			self.new_velocity=(self.new_velocity[0], self.new_velocity[1]+2*math.pi)
		
		self.new_velocity=(self.new_velocity[0]*(1-1e-3),self.new_velocity[1])

	def get_color(self):
		if self.charge>0:
			return (255,0,0)
		elif self.spin<0:
			return (0,0,255)
		elif self.spin>0:
			return (0,255,0)
		else:
			return (255,255,255)
