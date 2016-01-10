import item

class Orb(item.Item):
	def __init__(self, pos):
		super(Orb, self).__init__()
		self.image=super(Orb, self).init_image('Images/orb.png')
		self.rect=self.image.get_rect().move(pos)
	def act(self, p):
		p.orbs+=1
