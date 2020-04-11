import pygame as pg
from settings import *
from sprites import *
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
        self.map_data = []
        with open(path.join(game_folder, "map.txt"), 'rt') as f:
            for line in f:
                self.map_data.append(line)

        self.player_img = pg.image.load("images/player.png")
        self.empty_player_img = pg.image.load("images/player_transparent.png")
        self.enemy_img  = pg.image.load("images/enemy.png")
        self.wall_img = pg.image.load("images/wall.png")
        self.floor_img = pg.image.load("images/floor.png")

    def new(self):
        self.sprite_list = pg.sprite.LayeredUpdates()
        self.bullet_list = pg.sprite.Group()
        self.wall_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()

        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "w":
                    wall = Wall(self, col*TILE_SIZE, row*TILE_SIZE)
                elif tile == "p":
                    self.player = Player(self, col*TILE_SIZE, row*TILE_SIZE)
                elif tile == "e":
                    enemy = Enemy(self, col*TILE_SIZE, row*TILE_SIZE, ENEMY_HP)

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

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        self.sprite_list.draw(self.screen)
        pg.display.flip()

    def draw_grid(self):
        for x in range(0, WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x,0), (x,HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0,y), (WIDTH, y))
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if (event.button == 1):
                    player_x, player_y = self.player.rect.center
                    mouse_x, mouse_y = pg.mouse.get_pos()

                    delta_x = mouse_x - player_x
                    delta_y = mouse_y - player_y
                    theta = atan2(delta_y, delta_x)

                    ##create a bullet firing in the mouse direction
                    bullet_x = player_x + 10*cos(theta + 0.55)
                    bullet_y = player_y + 10*sin(theta + 0.55)
                    bullet = Bullet(self, bullet_x, bullet_y, theta - .01)
                
    def show_start_screen(self):
        pass

game = Game()
game.show_start_screen()
while True:
    game.new()
    game.run()
