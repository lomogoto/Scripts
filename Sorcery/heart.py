import item

class Heart(item.Item):
	def __init__(self, pos):
		super(Heart, self).__init__()
		self.image=super(Heart, self).init_image('Images/heart.png')
		self.rect=self.image.get_rect().move(pos)
	def act(self, p):
		p.health+=1
