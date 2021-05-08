from random import choice
from math import hypot
from main.grid import CellType

class Destination:
    destination = None
    destination_doominos = False  # Is the current destination to the Doomino's

    total_deliveries = 0  # Total number of deliveries that the player has made so far

    def __init__(self, grid, player):
        self.grid = grid
        self.player = player

        self.generate_destination()

    def step(self):
        player_pos = self.player.get_grid_position()
        if player_pos[0] == self.destination[0] and player_pos[1] == self.destination[1]:
            print('Destination reached')
            if not self.destination_doominos:
                self.destination = self.grid.doominos_location
                self.destination_doominos = True
                self.total_deliveries += 1
            else:
                self.generate_destination()
                self.destination_doominos = False

    def generate_destination(self):
        houses = self.grid.get_grid_cells_of_type(CellType.BUILDING)
        player_pos = self.player.get_grid_position()
        min_range = 10 + self.total_deliveries * 4
        max_range = 15 + self.total_deliveries * 8
        houses_in_range = [house for house in houses if min_range <= hypot(player_pos[0] - house.x, player_pos[1] - house.y) <= max_range]
        destination_house = choice(houses_in_range)
        self.destination = (destination_house.x, destination_house.y)
