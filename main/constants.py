class Constant:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FRAME_RATE = 60

    TILE_SIZE = 256

    GRID_WIDTH = 80
    GRID_HEIGHT = 80

    DELIVERY_TIME = 60
    DELIVERY_FINISHING_TIME = 5

    DELIVERY_PROFIT = 10
    DELIVERY_TIP = 10

    PLAYER_SPEED = 4
    PLAYER_SPEED_SKATEBOARD = 8
    PLAYER_SPEED_GRASS_MULTIPLIER = 0.6
    PLAYER_SPEED_SLOW_WALKING_MULTIPLIER = 0.3

    ZOMBIE_SPEED = 2
    MAX_ZOMBIE_SPEED = 3

    SCORE_SUBMIT_URL = 'http://gamejam2021.nl/submit2021.php'

    SLOT_WIDTH = 50
    SLOT_HEIGHT = 50

    FLAMETHROWER_FUEL = 1000

    # ============= SPAWNING ======================
    # Indicates the range of tiles around the player where zombies etc are spawned
    GRID_SPAWN_RANGE = 6

    # ==== Spawn rates ===
    # Amount of zombies in a tile will be chosen between 0 and AVG_ZOMBIES_PER_TILE_DISTANCE_FROM_CENTER * tiles_from_center
    AVG_ZOMBIES_PER_TILE_DISTANCE_FROM_CENTER = 0.25
    BLUE_ZOMBIE_PROB_INCREASE_PER_TILE_DISTANCE_FROM_CENTER = 0.001
    DOG_PROB_INCREASE_PER_TILE_DISTANCE_FROM_CENTER = 0.0005
