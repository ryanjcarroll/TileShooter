import pygame as pg
from settings import *
from pygame import Vector2 as vec

class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        """
        Initialize a new floor tile object.

        game    : the Game object to add the floor tile to.
        x       : x tile position.
        y       : y tile position.
        """
        self.groups = game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        game.sprite_list.change_layer(self, WALL_LAYER)

        self.game = game
        self.image = self.game.floor_img
        self.rect = self.image.get_rect()

        self.pos = vec(x + TILE_SIZE / 2, y + TILE_SIZE / 2)
        self.rect.center = self.pos