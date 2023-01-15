import pygame as pg
from settings import *
from map import *
from os import path
import sys

from sprites.Wall import Wall
from sprites.Player import Player
from sprites.Spawner import Spawner
from sprites.Enemy import Enemy
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
        spawner_folder = path.join(img_folder, "spawner")
        self.map = Map(path.join(map_folder, "map5.txt"))

        self.player_img = pg.image.load(path.join(img_folder, "player.png"))
        self.empty_player_img = pg.image.load(path.join(img_folder, "player_transparent.png"))
        self.enemy_img  = pg.image.load(path.join(img_folder, "2.png"))
        self.wall_img = pg.image.load(path.join(img_folder, "wall.png"))
        self.spawner_img = pg.image.load(path.join(img_folder, "spawner.png")).convert_alpha()

        self.enemy_move = [pg.image.load("images/2.png"), pg.image.load("images/3.png"), pg.image.load("images/4.png"), pg.image.load("images/5.png"), pg.image.load("images/6.png"), pg.image.load("images/7.png"), pg.image.load("images/8.png"), pg.image.load("images/9.png"), pg.image.load("images/10.png"),
                                pg.image.load("images/11.png"), pg.image.load("images/12.png"), pg.image.load("images/13.png"), pg.image.load("images/14.png"), pg.image.load("images/15.png"), pg.image.load("images/16.png"), pg.image.load("images/17.png"), pg.image.load("images/18.png"), pg.image.load("images/19.png"), pg.image.load("images/20.png"),
                                pg.image.load("images/21.png"), pg.image.load("images/22.png"), pg.image.load("images/23.png"), pg.image.load("images/24.png"), pg.image.load("images/25.png"), pg.image.load("images/26.png")]
        self.enemy_idle = [pg.image.load("images/2.png")]

        self.spawner_blast = [pg.image.load(path.join(spawner_folder, "new_spawn1.png")), pg.image.load(path.join(spawner_folder, "new_spawn2.png")), pg.image.load(path.join(spawner_folder, "new_spawn3.png")), pg.image.load(path.join(spawner_folder, "new_spawn4.png")), pg.image.load(path.join(spawner_folder, "new_spawn5.png")), pg.image.load(path.join(spawner_folder, "new_spawn6.png")), pg.image.load(path.join(spawner_folder, "new_spawn7.png")),
                           pg.image.load(path.join(spawner_folder, "new_spawn8.png")), pg.image.load(path.join(spawner_folder, "new_spawn9.png")), pg.image.load(path.join(spawner_folder, "new_spawn10.png")), pg.image.load(path.join(spawner_folder, "new_spawn11.png")), ]

    def new(self):
        self.sprite_list = pg.sprite.LayeredUpdates()
        self.bullet_list = pg.sprite.Group()
        self.wall_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()
        self.spawner_list = pg.sprite.Group()

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "w":
                    wall = Wall(self, col*TILE_SIZE, row*TILE_SIZE)
                elif tile == "p":
                    self.player = Player(self, col*TILE_SIZE, row*TILE_SIZE)
                elif tile == "e":
                    enemy = Enemy(self, col*TILE_SIZE, row*TILE_SIZE, ENEMY_HP)
                elif tile == "s":
                    spawner = Spawner(self, col*TILE_SIZE, row*TILE_SIZE, SPAWNER_RATE, SPAWNER_CAP, SPAWNER_RANGE, SPAWNER_HP, SPAWNER_DELAY)

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

    def start_screen(self):
        pass

    def game_over_screen(self):
        pass

game = Game()
game.start_screen()
while True:
    game.new()
    game.run()
