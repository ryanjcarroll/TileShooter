import pygame as pg
from math import atan2, degrees, cos, sin, sqrt
from settings import *
from pygame import Vector2 as vec

##returns true if the given circle and rectangle are collided
def circle_rect_collided(c, r):
    cx = c.x
    cy = c.y
    rx = r.rect.x
    ry = r.rect.y
    test_x = cx
    test_y = cy

    if (cx < rx):
        test_x = rx
    elif (cx > rx + r.rect.width):
        test_x = rx + r.rect.width

    if (cy < ry):
        test_y = ry
    elif (cy > ry + r.rect.height):
        test_y = ry + r.rect.height

    dist_x = cx - test_x
    dist_y = cy - test_y
    distance = sqrt(dist_x ** 2 + dist_y ** 2)
    if (distance <= c.width / 2):
        return True
    else:
        return False

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)

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
        move_x = vx * self.game.dt
        move_y = vy * self.game.dt
        self.x += move_x
        self.y += move_y

        ##undo if results in a wall collision
        if(self.wall_collision()):
            self.x -= move_x
            self.y -= move_y

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

    def wall_collision(self):
        b = False
        for wall in self.game.wall_list:
            if(circle_rect_collided(self, wall)):
                b = True
                break
        return b

    def check_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.move(-PLAYER_SPEED, 0)
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.move(PLAYER_SPEED, 0)
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.move(0, -PLAYER_SPEED)
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.move(0, PLAYER_SPEED)

    def update(self):
        self.check_keys()
        self.rotate()

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y, angle):
        self.groups = game.bullet_list, game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.angle = angle
        self.image = pg.Surface([4, 4])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed_magnitude = BULLET_SPEED

        self.x, self.y = x,y
        self.rect.center = int(self.x), int(self.y)

        self.speed = [self.speed_magnitude * cos(self.angle),
                      self.speed_magnitude * sin(self.angle)]

    def wall_collision(self):
        if pg.sprite.spritecollideany(self, self.game.wall_list):
            self.kill()

    def out_of_bounds(self):
        if(self.x < 0 or self.y < 0 or self.x > WIDTH or self.y > HEIGHT):
            self.kill()


    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

        self.rect.center = (int(self.x), int(self.y))

        self.wall_collision()
        self.out_of_bounds()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.wall_list, game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(LIGHT_GREY)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.enemy_list, game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.vel = vec(0,0)

    def move(self):
        for enemy in game.enemy_list:
            if(enemy != self):
                pass          ##TODO not done here


