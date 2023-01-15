import pygame as pg
from settings import *
from _utility import *
from math import cos, sin
from pygame import Vector2 as vec

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y, angle):
        self.groups = game.bullet_list, game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        game.sprite_list.change_layer(self, BULLET_LAYER)

        self.game = game
        self.angle = angle
        self.image = pg.Surface([4, 4])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed_magnitude = BULLET_SPEED
        self.damage = BULLET_DAMAGE

        self.pos = vec(x,y)
        self.orig_pos = vec(x,y)
        self.rect.center = self.pos

        self.vel = vec(self.speed_magnitude * cos(self.angle),
                      self.speed_magnitude * sin(self.angle))
        self.vel.normalize()
        self.vel *= BULLET_SPEED

    def wall_collision(self):
        if pg.sprite.spritecollideany(self, self.game.wall_list):
            self.kill()

    def spawner_collision(self):
        for spawner in self.game.spawner_list:
            if pg.sprite.collide_rect(self, spawner):
                spawner.hp -= self.damage
                self.kill()

    def out_of_bounds(self):
        if(self.pos.x < 0 or self.pos.y < 0 or self.pos.x > self.game.map.width or self.pos.y > self.game.map.height):
            self.kill()
        if (self.pos - self.orig_pos).length() > BULLET_RANGE:
            self.kill()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.wall_collision()
        self.spawner_collision()
        self.out_of_bounds()