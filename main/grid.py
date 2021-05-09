from random import randint, shuffle
from enum import Enum

import pygame

from main.constants import Constant
from main.util import convert_world_to_grid_position

images = {
    'GRASS1': {
        0: pygame.image.load("./resources/png/tiles/grass_1.png")
    },
    'GRASS2': {
        0: pygame.image.load("./resources/png/tiles/grass_2.png")
    },
    'GRASS3': {
        0: pygame.image.load("./resources/png/tiles/grass_3.png")
    },
    'GRASS4': {
        0: pygame.image.load("./resources/png/tiles/grass_4.png")
    },
    'GRASS5': {
        0: pygame.image.load("./resources/png/tiles/grass_5.png")
    },
    'GRASS6': {
        0: pygame.image.load("./resources/png/tiles/playground.png")
    },
    'HOUSE1': {
        0: pygame.image.load("./resources/png/tiles/house_1.png")
    },
    'HOUSE2': {
        0: pygame.image.load("./resources/png/tiles/house_2.png")
    },
    'HOUSE3': {
        0: pygame.image.load("./resources/png/tiles/house_3.png")
    },
    'HOUSE4': {
        0: pygame.image.load("./resources/png/tiles/house_4.png")
    },
    'INTERSECTION': {
        0: pygame.image.load("./resources/png/tiles/street_intersection.png")
    },
    'TSECTION': {
        0: pygame.image.load("./resources/png/tiles/street_t_section.png")
    },
    'CORNER': {
        0: pygame.image.load("./resources/png/tiles/street_corner.png")
    },
    'STRAIGHT1': {
        0: pygame.image.load("./resources/png/tiles/street_straight_1.png")
    },
    'STRAIGHT2': {
        0: pygame.image.load("./resources/png/tiles/street_straight_2.png")
    },
    'DEADEND': {
        0: pygame.image.load("./resources/png/tiles/street_dead_end.png")
    },
    'DOOMINOS': {
        0: pygame.image.load("./resources/png/tiles/doominos.png")
    }
}


def get_image(image, rotation=0):
    if image == 'GRASS':
        image += str(randint(1, 6))
    elif image == 'HOUSE':
        image += str(randint(1, 4))
    elif image == 'STRAIGHT':
        variant = 2 if randint(1, 10) == 1 else 1
        image += str(variant)

    if image not in images:
        print(image, 'not found')
        return None
    if rotation not in images[image]:
        images[image][rotation] = pygame.transform.rotate(images[image][0], rotation)
    return images[image][rotation]


class CellType(Enum):
    EMPTY = 0
    BUILDING = 1
    ROAD = 2
    NATURE = 3
    DOOMINOS = 4

    @staticmethod
    def surface_of(cell_type, rotation=0):
        if cell_type == CellType.BUILDING:
            return get_image('HOUSE', rotation)
        elif cell_type == CellType.ROAD:
            return get_image('STRAIGHT', rotation)
        elif cell_type == CellType.DOOMINOS:
            return get_image('DOOMINOS', rotation)
        elif cell_type == CellType.NATURE or cell_type == CellType.EMPTY:
            return get_image('GRASS', rotation)


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


inaccessible_tiles = {CellType.DOOMINOS, CellType.BUILDING}


class Grid:
    doominos_location = None

    def __init__(self, width, height, world):
        """
        Initialize the grid
        :param width: width of the grid
        :param height: height of the grid
        """
        self.world = world
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

    def get_grid_cells_of_type(self, type):
        """
        Get all grid cells of the specified type
        :param type: type of the cell
        :type type: CellType
        :return: list of cells
        :rtype: [Cell]
        """
        cells = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.grid[x][y].type == type:
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

        self.align_roads()
        self.align_tiles()

    def generate_roads(self):
        """
        Generate the roads and areas on the map
        """
        cells = self.get_grid_cells()
        shuffle(cells)

        area_min = 4  # Minimum size of the area
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
                if self.is_in_grid(x, y + 1) and self.grid[x][y + 1].id != self.grid[x][y].id:
                    self.grid[x][y].type = CellType.ROAD

    def align_roads(self):
        # Generate the correct surfaces for the road pieces
        for x in range(self.width):
            for y in range(self.height):
                if not self.grid[x][y].type == CellType.ROAD:
                    continue
                if self.is_in_grid(x, y + 1) and self.grid[x][y + 1].type == CellType.ROAD:
                    # BOTTOM
                    if self.is_in_grid(x + 1, y) and self.grid[x + 1][y].type == CellType.ROAD:
                        # BOTTOM, RIGHT
                        if self.is_in_grid(x, y - 1) and self.grid[x][y - 1].type == CellType.ROAD:
                            # BOTTOM, RIGHT, TOP
                            if self.is_in_grid(x - 1, y) and self.grid[x - 1][y].type == CellType.ROAD:
                                # BOTTOM, RIGHT, TOP, LEFT
                                # =R=
                                # RRR  INTERSECTION
                                # =R=
                                self.grid[x][y].surface = get_image("INTERSECTION")
                            else:  # BOTTOM, RIGHT, TOP
                                # =R=
                                # =RR  TSECTION
                                # =R=
                                self.grid[x][y].surface = get_image("TSECTION", 90)
                        else:  # BOTTOM, RIGHT
                            if self.is_in_grid(x - 1, y) and self.grid[x - 1][y].type == CellType.ROAD:
                                # BOTTOM, RIGHT, LEFT
                                # ===
                                # RRR  TSECTION
                                # =R=
                                self.grid[x][y].surface = get_image("TSECTION")
                            else:  # BOTTOM, RIGHT
                                # ===
                                # =RR  CORNER
                                # =R=
                                self.grid[x][y].surface = get_image("CORNER", 90)
                    else:  # BOTTOM
                        if self.is_in_grid(x, y - 1) and self.grid[x][y - 1].type == CellType.ROAD:
                            # BOTTOM, TOP
                            if self.is_in_grid(x - 1, y) and self.grid[x - 1][y].type == CellType.ROAD:
                                # BOTTOM, TOP, LEFT
                                # =R=
                                # RR=  TSECTION
                                # =R=
                                self.grid[x][y].surface = get_image("TSECTION", -90)
                            else:  # BOTTOM, TOP
                                # =R=
                                # =R=  STRAIGHT
                                # =R=
                                self.grid[x][y].surface = get_image("STRAIGHT")
                        else:  # BOTTOM
                            if self.is_in_grid(x - 1, y) and self.grid[x - 1][y].type == CellType.ROAD:
                                # BOTTOM, LEFT
                                # ===
                                # RR=  CORNER
                                # =R=
                                self.grid[x][y].surface = get_image("CORNER")
                            else:  # BOTTOM
                                # ===
                                # =R=  DEADEND
                                # =R=
                                self.grid[x][y].surface = get_image("DEADEND")
                else:  # -nothing-
                    if self.is_in_grid(x + 1, y) and self.grid[x + 1][y].type == CellType.ROAD:
                        # RIGHT
                        if self.is_in_grid(x, y - 1) and self.grid[x][y - 1].type == CellType.ROAD:
                            # RIGHT, TOP
                            if self.is_in_grid(x - 1, y) and self.grid[x - 1][y].type == CellType.ROAD:
                                # RIGHT, TOP, LEFT
                                # =R=
                                # RRR  TSECTION
                                # ===
                                self.grid[x][y].surface = get_image("TSECTION", 180)
                            else:  # RIGHT, TOP
                                # =R=
                                # =RR  CORNER
                                # ===
                                self.grid[x][y].surface = get_image("CORNER", 180)
                        else:  # RIGHT
                            if self.is_in_grid(x - 1, y) and self.grid[x - 1][y].type == CellType.ROAD:
                                # RIGHT, LEFT
                                # ===
                                # RRR  STRAIGHT
                                # ===
                                self.grid[x][y].surface = get_image("STRAIGHT", 90)
                            else:  # RIGHT
                                # ===
                                # =RR  DEADEND
                                # ===
                                self.grid[x][y].surface = get_image("DEADEND", 90)
                    else:  # -nothing-
                        if self.is_in_grid(x, y - 1) and self.grid[x][y - 1].type == CellType.ROAD:
                            # TOP
                            if self.is_in_grid(x - 1, y) and self.grid[x - 1][y].type == CellType.ROAD:
                                # TOP, LEFT
                                # =R=
                                # RR=  CORNER
                                # ===
                                self.grid[x][y].surface = get_image("CORNER", 270)
                            else:  # TOP
                                # =R=
                                # =R=  DEADEND
                                # ===
                                self.grid[x][y].surface = get_image("DEADEND", 180)
                        else:  # -nothing-
                            if self.is_in_grid(x - 1, y) and self.grid[x - 1][y].type == CellType.ROAD:
                                # LEFT
                                # ===
                                # RR=  DEADEND
                                # ===
                                self.grid[x][y].surface = get_image("DEADEND", -90)
                            else:  # -nothing-
                                # ===
                                # =R=  STRAIGHT
                                # ===
                                self.grid[x][y].surface = get_image("STRAIGHT", 90)

    def align_tiles(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].type == CellType.DOOMINOS or self.grid[x][y].type == CellType.BUILDING:
                    if self.is_in_grid(x, y - 1) and self.grid[x][y - 1].type == CellType.ROAD:
                        # Rotate to TOP
                        self.grid[x][y].surface = pygame.transform.rotate(self.grid[x][y].surface, 180)
                    elif self.is_in_grid(x + 1, y) and self.grid[x + 1][y].type == CellType.ROAD:
                        # Rotate to RIGHT
                        self.grid[x][y].surface = pygame.transform.rotate(self.grid[x][y].surface, 90)
                    elif self.is_in_grid(x, y + 1) and self.grid[x][y + 1].type == CellType.ROAD:
                        # Rotate to BOTTOM (which means do nothing)
                        pass
                    elif self.is_in_grid(x - 1, y) and self.grid[x - 1][y].type == CellType.ROAD:
                        # Rotate to LEFT
                        self.grid[x][y].surface = pygame.transform.rotate(self.grid[x][y].surface, -90)

    def generate_doominoes(self):
        """
        Generate Doominos
        """
        doominoes_x = self.width // 2 + 1
        doominoes_y = self.height // 2 + 1
        self.grid[doominoes_x][doominoes_y].type = CellType.DOOMINOS
        self.grid[doominoes_x][doominoes_y].surface = CellType.surface_of(CellType.DOOMINOS)
        self.doominos_location = (doominoes_x, doominoes_y)

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
                road_until_x = None
                road_until_y = None
                while self.is_in_grid(x, y):
                    if self.is_connected_to(x, y, CellType.ROAD):
                        connected = True
                        road_until_x = x
                        road_until_y = y
                        break
                    x += x_delta
                    y += y_delta

                if not connected:
                    # Try a different direction
                    direction = (direction + 1) % 4
                    continue

                x = doominoes_x + x_delta
                y = doominoes_y + y_delta
                while True:
                    self.grid[x][y].type = CellType.ROAD
                    self.grid[x][y].surface = CellType.surface_of(CellType.ROAD)
                    if x == road_until_x and y == road_until_y:
                        break
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

    def draw(self, screen: pygame.Surface, camera):
        player_x, player_y = convert_world_to_grid_position(self.world.player.x, self.world.player.y)
        left_x = max(0, player_x - Constant.GRID_SPAWN_RANGE)
        right_x = min(Constant.GRID_WIDTH, player_x + Constant.GRID_SPAWN_RANGE)
        top_y = max(0, player_y - Constant.GRID_SPAWN_RANGE)
        bottom_y = min(Constant.GRID_HEIGHT, player_y + Constant.GRID_SPAWN_RANGE)

        for x in range(left_x, right_x):
            for y in range(top_y, bottom_y):
                current_cell = self.grid[x][y]
                camera.blit_surface_to_screen(screen, current_cell.surface, Constant.TILE_SIZE * x,
                                              Constant.TILE_SIZE * y, centered=False)

    def is_accessible(self, grid_x, grid_y):
        # The map is a jail, you cannot escape >:-)
        if not self.is_in_grid(grid_x, grid_y):
            return False

        return self.grid[grid_x][grid_y].type not in inaccessible_tiles
