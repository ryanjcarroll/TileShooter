import pygame as pg
from settings import *
from pygame import Vector2 as vec

class Animation(pg.sprite.Sprite):
    def __init__(self, game, x, y, list):
        self.groups = game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.pos = vec(x,y)
        self.list = list

        self.image = self.list[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.current = 0

    def update(self):
        if self.current < len(self.list) - 1:
            self.image = self.list[self.current]
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.current += 1
        else:
            self.kill()
