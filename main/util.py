from main.constants import Constant


def distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


def convert_world_to_grid_position(x, y):
    """
    Converts a position in the world to a grid position (the indices of tiles in the grid)
    :param x: Entity x position in world
    :param y: Entity y position in world
    :return: (grid_x, grid_y)
    """
    return int(x // Constant.TILE_SIZE), int(y // Constant.TILE_SIZE)


def can_move_to(x, y, grid):
    """
    Checks whether the given WORLD x and y coordinates can be moved to (wrt. the grid)
    :param x: World x to move to
    :param y: World y to move to
    :param grid: the grid containing the world map (main.Grid instance)
    :return: Boolean, whether one can move to the specified x and y locations
    """
    grid_x, grid_y = convert_world_to_grid_position(x, y)
    return grid.is_accessible(grid_x, grid_y)
