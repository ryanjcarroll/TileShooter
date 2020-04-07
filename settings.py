##colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (40, 40, 40)
LIGHT_GREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

##game settings
TILE_SIZE = 32
GRID_WIDTH = 32
GRID_HEIGHT = 24
WIDTH = GRID_WIDTH * TILE_SIZE
HEIGHT = GRID_HEIGHT * TILE_SIZE

TITLE = "my game"
BG_COLOR = DARK_GREY
FPS = 60

## player settings
PLAYER_SPEED = 200
BULLET_SPEED = 32

##enemy settings
ENEMY_SPEED = 100
AVOID_WALLS_RADIUS = 48
AVOID_WALLS_WEIGHT = 0.1
AVOID_ENEMIES_RADIUS = 48
AVOID_ENEMIES_WEIGHT = 0.2