import pygame as pg
from settings import *
from sprites import *
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
        pass

    def new(self):
        self.sprite_list = pg.sprite.Group()
        ##self.wall_list = pg.sprite.Group()
        self.player = Player(self, 0, 0)
        self.sprite_list.add(self.player)
        ##for x in range(10,20):
            ##Wall(self, x, 5)
        ##   pass

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
                
    def show_start_screen(self):
        pass

game = Game()
game.show_start_screen()
while True:
    game.new()
    game.run()
