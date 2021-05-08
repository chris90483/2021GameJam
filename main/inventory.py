from entities.flamethrower import Flamethrower

class Inventory(object):

    def __init__(self, player):
        self.flamethrower = Flamethrower(player)

    def step(self):
        self.flamethrower.step()

    def draw(self, screen, camera):
        pass

