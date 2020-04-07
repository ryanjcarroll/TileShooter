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
        self.bullet_list = pg.sprite.Group()
        self.player = Player(self, 50, 50)
        self.sprite_list.add(self.player)

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

        #remove out of bounds bullets
        for bullet in self.bullet_list:
            if(bullet.x < 0 or bullet.y < 0 or bullet.x > WIDTH or bullet.y > HEIGHT):
                self.sprite_list.remove(bullet)
                self.bullet_list.remove(bullet)

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
                    theta = -atan2(delta_y, delta_x)

                    ##create a bullet firing in the mouse direction
                    bullet = Bullet(player_x, player_y, -theta)
                    self.sprite_list.add(bullet)
                    self.bullet_list.add(bullet)
                
    def show_start_screen(self):
        pass

game = Game()
game.show_start_screen()
while True:
    game.new()
    game.run()
