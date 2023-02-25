import pygame as pg
from settings import *
from map import *
from os import path
import sys

from sprites.Wall import Wall
from sprites.Player import Player
from sprites.Spawner import Spawner
from sprites.Enemies.Enemy import Enemy
from sprites.Enemies.Zombie import Zombie
from sprites.Enemies.Devil import Devil
pg.init()

class Game:
    def __init__(self):
        """
        Initialize game object and settings.
        """
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        ##pg.key.set_repeat(500,100)  ##delays held down keys
        self.load_data()
        
    def load_data(self):
        """
        Set resource paths and load sprite images.
        """
        # set resource paths for game assets
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, "maps")
        img_folder = path.join(game_folder, "images")
        spawner_folder = path.join(img_folder, "spawner")

        # set map file
        self.map = Map(path.join(map_folder, "map5.txt"))

        # set sprites
        self.player_img = pg.image.load(path.join(img_folder, "player.png"))
        self.empty_player_img = pg.image.load(path.join(img_folder, "player_transparent.png"))
        self.zombie_img  = pg.image.load(path.join(img_folder, "2.png"))
        self.charger_img = pg.image.load(path.join(img_folder, "enemy.png"))
        self.wall_img = pg.image.load(path.join(img_folder, "wall.png"))
        self.spawner_img = pg.image.load(path.join(img_folder, "spawner.png")).convert_alpha()

        # set image lists for sprite animations
        self.spawner_blast = [pg.image.load(path.join(spawner_folder, f"new_spawn{i}.png")) for i in range(1,12,1)]

    def new(self):
        """
        Create a new game by initializing sprite lists and loading game objects based on the mapfile.
        """
        # lists of objects for the game to render
        self.sprite_list = pg.sprite.LayeredUpdates()
        self.bullet_list = pg.sprite.Group()
        self.wall_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()
        self.spawner_list = pg.sprite.Group()

        # load game objects based on the map file
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "w":
                    Wall(self, col*TILE_SIZE, row*TILE_SIZE)
                elif tile == "p":
                    self.player = Player(self, col*TILE_SIZE, row*TILE_SIZE)
                elif tile == "e":
                    Zombie(self, col*TILE_SIZE, row*TILE_SIZE)
                elif tile == "s":
                    Spawner(self, col*TILE_SIZE, row*TILE_SIZE, SPAWNER_RATE, SPAWNER_CAP, SPAWNER_RANGE, SPAWNER_HP, SPAWNER_DELAY)
                elif tile == "c":
                    Devil(self, col*TILE_SIZE, row*TILE_SIZE)

        # initialize a camera object with the selected map dimensions
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        """
        Main game loop.
        """
        self.playing = True
        while(self.playing):
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            
    def quit(self):
        """
        End the game.
        """
        pg.quit()
        sys.exit()

    def update(self):
        """
        Update sprites and camera.
        """
        self.sprite_list.update()
        self.camera.update(self.player)

    def draw(self):
        """
        Draw screen background, sprites, health and stamina bars.
        """
        self.screen.fill(BG_COLOR)
        #self.draw_grid()
        for sprite in self.sprite_list:
            if isinstance(sprite, Spawner):
                sprite.draw_health()
            if isinstance(sprite, Player):
                sprite.draw_health()
                sprite.draw_stamina()
            if isinstance(sprite, Enemy):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def draw_grid(self):
        """
        Utility/debugging method to draw gridlines over map assets.
        """
        for x in range(0, WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))
            
    def events(self):
        """
        Check for mouse events.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if (event.button == 1):
                    self.player.shoot()

    def start_screen(self):
        pass

    def game_over_screen(self):
        pass

# initialize a game object and start running
game = Game()
game.start_screen()
game.new()
game.run()
