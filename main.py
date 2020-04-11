import pygame as pg
from settings import *
from sprites import *
from map import *
from os import path
import sys
pg.init()

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        ##pg.key.set_repeat(500,100)  ##delays held down keys
        self.load_data()
        
    def load_data(self):
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, "maps")
        img_folder = path.join(game_folder, "images")
        self.map = Map(path.join(map_folder, "map2.txt"))

        self.player_img = pg.image.load(path.join(img_folder, "player.png"))
        self.empty_player_img = pg.image.load(path.join(img_folder, "player_transparent.png"))
        self.enemy_img  = pg.image.load(path.join(img_folder, "enemy.png"))
        self.wall_img = pg.image.load(path.join(img_folder, "wall.png"))
        self.floor_img = pg.image.load(path.join(img_folder, "floor.png"))

    def new(self):
        self.sprite_list = pg.sprite.LayeredUpdates()
        self.bullet_list = pg.sprite.Group()
        self.wall_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "w":
                    wall = Wall(self, col*TILE_SIZE, row*TILE_SIZE)
                elif tile == "p":
                    self.player = Player(self, col*TILE_SIZE, row*TILE_SIZE)
                elif tile == "e":
                    enemy = Enemy(self, col*TILE_SIZE, row*TILE_SIZE, ENEMY_HP)

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while(self.playing):
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.sprite_list.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BG_COLOR)
        #self.draw_grid()
        for sprite in self.sprite_list:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def draw_grid(self):
        for x in range(0, WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if (event.button == 1):
                    self.player.shoot()
                
    def show_start_screen(self):
        pass

game = Game()
game.show_start_screen()
while True:
    game.new()
    game.run()
