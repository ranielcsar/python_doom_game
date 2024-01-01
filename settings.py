import math

RES = WIDTH, HEIGHT = 1600, 900
FPS = 60

PLAYER_POSITION = 1.5, 5  # mini_map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROTATION_SPEED = 0.002

# RAYCASTING

# FOV is the field of view of the player
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2  # // stands for integer division
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20
