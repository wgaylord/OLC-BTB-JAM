class Entity:
	def __init__(self):
		pass




class Zombie(Entity):
    def __init__(self):
        self.health = 10.0
        self.x = 0
        self.y = 0
        self.attack_delay = 30