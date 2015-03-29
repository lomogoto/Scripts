class particle():
	def __init__(self, position, mass, charge, color=False, velocity=[0,0]):
		self.charge=charge
		self.color=color
		self.mass=mass
		self.position=position
		self.velocity=velocity

		self.new_position=[0,0]
		self.new_velocity=[0,0]

	def update(self):
		self.position=self.new_position
		self.velocity=self.new_velocity

	def apply_force(self, force):
		self.new_velocity=[self.velocity[0]+int(force[0]/self.mass),self.velocity[1]+int(force[1]/self.mass)]
		self.new_position=[self.position[0]+self.new_velocity[0], self.position[1]+self.new_velocity[1]]

	def get_color(self):
		if self.charge>0:
			return (255,0,0)
		elif self.charge<0:
			return (0,255,255)
		else:
			return (255,255,255)
