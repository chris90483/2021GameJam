from random import choice
from math import hypot
from main.grid import CellType
import time
from main.constants import Constant

class Destination:
    destination = None
    destination_doominos = False  # Is the current destination to the Doomino's
    delivering = None

    total_deliveries = 0  # Total number of deliveries that the player has made so far

    def __init__(self, grid, player):
        self.grid = grid
        self.player = player

        self.__generate_destination()

    def step(self):
        if self.__player_at_delivery_location():
            if self.delivering is None:
                # Set the current time as the delivery start time and wait for Constant.DELIVERY_TIME
                self.delivering = time.time()
            elif time.time() - self.delivering >= Constant.DELIVERY_TIME:
                # Update the delivery destination
                self.delivering = None
                if not self.destination_doominos:
                    self.destination = self.grid.doominos_location
                    self.destination_doominos = True
                    self.total_deliveries += 1
                else:
                    self.__generate_destination()
                    self.destination_doominos = False
        else:
            self.delivering = None

    def __player_at_delivery_location(self):
        """
        Check if the player is at the delivery location
        :return: true if the player is at the location, false otherwise
        """
        player_location = self.player.get_grid_position(False)
        return self.destination[0] - 0.5 < player_location[0] < self.destination[0] + 1.5 and self.destination[1] - 0.5 < player_location[1] < self.destination[1] + 1.5

    def __generate_destination(self):
        """
        Generate a new delivery location
        """
        houses = self.grid.get_grid_cells_of_type(CellType.BUILDING)
        player_pos = self.player.get_grid_position()
        min_range = 10 + self.total_deliveries * 4
        max_range = 15 + self.total_deliveries * 8
        houses_in_range = []
        while len(houses_in_range) == 0:
            houses_in_range = [house for house in houses if min_range <= hypot(player_pos[0] - house.x, player_pos[1] - house.y) <= max_range]
            max_range += 5
        destination_house = choice(houses_in_range)
        self.destination = (destination_house.x, destination_house.y)

    def get_delivery_progress(self):
        """
        Return the progress of the delivery on a scale from 0 (not delivered) to 1 (delivered)
        :return: delivery progress
        """
        if self.delivering is None:
            return 0
        else:
            return min(1, (time.time() - self.delivering) / Constant.DELIVERY_TIME)
