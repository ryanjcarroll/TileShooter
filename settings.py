from pygame import Rect

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
PLAYER_HITBOX = Rect(0, 0, 15, 15)
PLAYER_HEALTHBAR_SIZE = 64
PLAYER_HP = 100
PLAYER_HIT_TIME= 60 ##hit animation length, in frames
PLAYER_RESPAWN_TIME = 60 ##invincibility after death, in frames

##bullet settings
BULLET_SPEED = 32
BULLET_RANGE = 512
BULLET_DAMAGE = 10
KNOCKBACK = 0.1

##enemy settings
ENEMY_SPEED = 400
ENEMY_HP = 40
ENEMY_DAMAGE = 25
ENEMY_HITBOX = Rect(0,0,15,15)
ENEMY_WAIT = 60 ##frames to do nothing before chasing player
AVOID_WALLS_RADIUS = 48
AVOID_WALLS_WEIGHT = 1.5
AVOID_ENEMIES_RADIUS = 48
AVOID_ENEMIES_WEIGHT = 1
AGGRO_RADIUS = 1000
WALL_BOUNCE = 0.5

##layer settings
PLAYER_LAYER = 2
ENEMY_LAYER = 3
WALL_LAYER = 1
BULLET_LAYER = 4

##spawner settings
SPAWNER_HP = 400
SPAWNER_RANGE = 100
SPAWNER_CAP = 3
SPAWNER_RATE = 180
SPAWNER_DELAY = 10
SPAWNER_HITBOX = Rect(0,0,32,32)
SPAWNER_BUFFER = 34 ##pixels to allow between a spawned enemy and nearby blocks
SPAWN_ATTEMPTS = 50 ##maximum times the spawner will attempt to find valid locations each iteration
MAX_ENEMIES = 40