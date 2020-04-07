import pygame as pg
from math import atan2, degrees, cos, sin
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)

        self.x = x ##non int-deprecated position
        self.y = y

        self.image = pg.image.load("images/circle.png")
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.game = game

        self.rect.x = int(self.x - self.rect.width / 2)
        self.rect.y = int(self.y - self.rect.height / 2)
        self.vx, self.vy = 0,0

    def move(self, vx, vy):
        self.x += vx * self.game.dt
        self.y += vy * self.game.dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def rotate(self):
        player_x, player_y = self.x, self.y
        mouse_x, mouse_y = pg.mouse.get_pos()

        delta_x = mouse_x - player_x
        delta_y = mouse_y - player_y
        angle = -atan2(delta_y, delta_x)

        deg = degrees(angle)

        new_image = pg.image.load("images/circle.png")
        rotated_image = pg.transform.rotate(new_image, deg)
        new_rect = rotated_image.get_rect()

        self.image = rotated_image
        self.rect = new_rect

        self.rect.center = player_x, player_y

    def draw_line(self, x, y):
        center_x, center_y = self.rect.center
        pg.draw.line(self.game.screen, WHITE, (center_x, center_y), (x, y))

    def check_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.vy = PLAYER_SPEED

    def update(self):
        self.check_keys()
        self.move(self.vx, self.vy)
        self.rotate()

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, angle):
        pg.sprite.Sprite.__init__(self)

        self.angle = angle
        self.image = pg.Surface([4, 4])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed_magnitude = BULLET_SPEED

        self.x, self.y = x,y
        self.rect.center = int(self.x), int(self.y)

        self.speed = [self.speed_magnitude * cos(self.angle),
                      self.speed_magnitude * sin(self.angle)]

    def update(self):
        ##update the stored position without int conversion
        self.x += self.speed[0]
        self.y += self.speed[1]
        ##update the displayed position as an int(pixel) value
        self.rect.center = (int(self.x), int(self.y))