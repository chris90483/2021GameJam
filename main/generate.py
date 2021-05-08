from random import randint, shuffle
from enum import Enum

import pygame

from main.camera import Camera
from main.constants import Constant


class CellType(Enum):
    EMPTY = 0
    BUILDING = 1
    ROAD = 2
    NATURE = 3
    DOOMINOS = 4

    def surface_of(cell_type):
        if cell_type == CellType.EMPTY:
            return pygame.image.load("./resources/png/tiles/grass.png")
        elif cell_type == CellType.BUILDING:
            return pygame.image.load("./resources/png/tiles/house_1.png")
        elif cell_type == CellType.ROAD:
            return pygame.image.load("./resources/png/tiles/street_intersection.png")
        elif cell_type == CellType.NATURE:
            return pygame.image.load("./resources/png/tiles/grass.png")
        elif cell_type == CellType.DOOMINOS:
            return pygame.image.load("./resources/png/tiles/doominos.png")


class Cell:
    type = None
    id = None
    surface = None

    def __init__(self, x, y):
        """
        Initialize a grid cell
        :param x: x coordinate of the grid cell
        :param y: y coordinate of the grid cell
        """
        self.x = x
        self.y = y


class Grid:
    def __init__(self, width, height):
        """
        Initialize the grid
        :param width: width of the grid
        :param height: height of the grid
        """
        # Create empty grid
        self.width = width
        self.height = height
        self.grid = []
        for x in range(width):
            column = []
            for y in range(height):
                column.append(Cell(x, y))
            self.grid.append(column)

        self.generate()

    def get_grid_cells(self):
        """
        Get a list of all the even grid cells
        """
        cells = []
        for x in range(0, self.width, 2):
            for y in range(0, self.height, 2):
                cells.append(self.grid[x][y])
        return cells

    def is_in_grid(self, x, y):
        """
        Checks if the specified coordinate is a valid coordinate
        :param x: x coordinate of the grid cell
        :param y: y coordinate of the grid cell
        :return: true if a grid cell exists with the specified coordinates, false otherwise
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def is_connected_to(self, x, y, type):
        """
        Check if a grid cell is connected to a specific type of cell
        :param x: x coordinate of the grid cell
        :param y: y coordinate of the grid cell
        :param type: type of the adjacent grid cell to use for
        :return: true if an adjacent cell with the specified type was found, false otherwise
        """
        return (x + 1 < self.width and self.grid[x + 1][y].type == type) or \
               (x - 1 >= 0 and self.grid[x - 1][y].type == type) or \
               (y + 1 < self.height and self.grid[x][y + 1].type == type) or \
               (y - 1 >= 0 and self.grid[x][y - 1].type == type)

    def generate(self):
        """
        Generate a map
        """
        self.generate_roads()
        self.generate_doominoes()
        self.generate_buildings_and_nature()

    def generate_roads(self):
        """
        Generate the roads and areas on the map
        """
        cells = self.get_grid_cells()
        shuffle(cells)

        area_min = 3  # Minimum size of the area
        area_max = 10  # Maximum size of the long side of the area

        # For each cell in the map, generate an area of a random size if it is not in an area yet
        for area_id in range(len(cells)):
            cell = cells[area_id]
            if cell.type is None:
                direction = randint(0, 1)
                area_width = randint(area_min, area_max if direction else area_min)
                area_height = randint(area_min, area_min if direction else area_max)

                for i in range(0, area_width, 2):
                    for j in range(0, area_height, 2):
                        if self.is_in_grid(cell.x + i + 1, cell.y + j + 1):
                            self.grid[cell.x + i][cell.y + j].id = area_id
                            self.grid[cell.x + i][cell.y + j].type = CellType.EMPTY
                            self.grid[cell.x + i][cell.y + j].surface = CellType.surface_of(CellType.EMPTY)

                            self.grid[cell.x + i + 1][cell.y + j].id = area_id
                            self.grid[cell.x + i + 1][cell.y + j].type = CellType.EMPTY
                            self.grid[cell.x + i + 1][cell.y + j].surface = CellType.surface_of(CellType.EMPTY)

                            self.grid[cell.x + i][cell.y + j + 1].id = area_id
                            self.grid[cell.x + i][cell.y + j + 1].type = CellType.EMPTY
                            self.grid[cell.x + i][cell.y + j + 1].surface = CellType.surface_of(CellType.EMPTY)

                            self.grid[cell.x + i + 1][cell.y + j + 1].id = area_id
                            self.grid[cell.x + i + 1][cell.y + j + 1].type = CellType.EMPTY
                            self.grid[cell.x + i + 1][cell.y + j + 1].surface = CellType.surface_of(CellType.EMPTY)

        # For each cell that is on the border between two areas, change the cell type to road
        for x in range(self.width):
            for y in range(self.height):
                if self.is_in_grid(x + 1, y) and self.grid[x + 1][y].id != self.grid[x][y].id:
                    self.grid[x][y].type = CellType.ROAD
                    self.grid[x][y].surface = CellType.surface_of(CellType.ROAD)
                if self.is_in_grid(x, y + 1) and self.grid[x][y + 1].id != self.grid[x][y].id:
                    self.grid[x][y].type = CellType.ROAD
                    self.grid[x][y].surface = CellType.surface_of(CellType.ROAD)

    def generate_doominoes(self):
        """
        Generate Doominos
        """
        doominoes_x = self.width // 2 + 1
        doominoes_y = self.height // 2 + 1
        self.grid[doominoes_x][doominoes_y].type = CellType.DOOMINOS
        self.grid[doominoes_x][doominoes_y].surface = CellType.surface_of(CellType.DOOMINOS)

        if not self.is_connected_to(doominoes_x, doominoes_y, CellType.ROAD):
            direction = randint(0, 3)
            connected = False
            while not connected:
                x_delta = 0
                if direction == 0:
                    x_delta = -1
                elif direction == 1:
                    x_delta = 1
                x = doominoes_x + x_delta

                y_delta = 0
                if direction == 2:
                    y_delta = -1
                elif direction == 3:
                    y_delta = 1
                y = doominoes_y + y_delta

                # Check if there is a road in this direction
                while self.is_in_grid(x, y):
                    if self.is_connected_to(x, y, CellType.ROAD):
                        connected = True
                        break
                    x += x_delta
                    y += y_delta

                if not connected:
                    # Try a different direction
                    direction = (direction + 1) % 4
                    continue

                x = doominoes_x + x_delta
                y = doominoes_y + y_delta
                while not self.is_connected_to(x, y, CellType.ROAD):
                    self.grid[x][y].type = CellType.ROAD
                    self.grid[x][y].surface = CellType.surface_of(CellType.ROAD)
                    x += x_delta
                    y += y_delta

    def generate_buildings_and_nature(self):
        """
        Generate buildings and nature in the empty spaces
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].type == CellType.EMPTY:
                    cell_type = CellType.NATURE
                    if self.is_connected_to(x, y, CellType.ROAD):
                        # Connected to road, choose between building and nature
                        if randint(0, 1):
                            cell_type = CellType.BUILDING
                    self.grid[x][y].type = cell_type
                    self.grid[x][y].surface = CellType.surface_of(cell_type)

    def print_grid(self):
        """
        Print the grid to standard out
        :return:
        """
        for y in range(self.height):
            for x in range(self.width):
                item = self.grid[x][y]
                if item.type == CellType.DOOMINOS:
                    print('🍕', end='')
                elif item.type == CellType.BUILDING:
                    print('🏡', end='')
                elif item.type == CellType.ROAD:
                    print('░░', end='')
                elif item.type == CellType.NATURE:
                    print('🌴', end='')
                else:
                    print('  ', end='')
            print('')

    def draw(self, screen: pygame.Surface, camera: Camera):
        for x in range(0, self.width):
            for y in range(0, self.height):
                current_cell = self.grid[x][y]
                camera.blit_surface_to_screen(screen, current_cell.surface, Constant.TILE_SIZE * x, Constant.TILE_SIZE * y)
