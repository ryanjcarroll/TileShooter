import pygame as pg
from settings import *
from pygame import Vector2 as vec

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.wall_list, game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        game.sprite_list.change_layer(self, WALL_LAYER)

        self.game = game
        self.image = self.game.wall_img
        self.rect = self.image.get_rect()

        self.pos = vec(x + TILE_SIZE/2, y + TILE_SIZE/2)
        self.rect.center = self.pos