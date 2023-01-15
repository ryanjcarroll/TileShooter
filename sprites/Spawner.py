import pygame as pg
from settings import *
from ._utility import *
from .Enemy import Enemy
from .Animation import Animation
import random
from pygame import Vector2 as vec

class Spawner(pg.sprite.Sprite):
    def __init__(self, game, x, y, rate, cap, range, hp, delay):
        self.groups = game.spawner_list, game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        game.sprite_list.change_layer(self, WALL_LAYER)
        self.game = game

        self.pos = vec(x, y + TILE_SIZE)

        self.image = self.game.spawner_img
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.pos
        self.width = self.rect.width
        self.hitbox = SPAWNER_HITBOX
        self.hitbox.center = self.rect.center

        self.rate = rate    ##how many seconds to pass between spawns
        self.count = 0
        self.cap = cap #zombies per spawn
        self.range = range  ##radius of eligible spawn locations
        self.delay = delay ##ticks to wait until first spawn

        self.hp = hp

    def spawn_enemies(self):
        self.enemies_spawned = 0

        num_tries = 0
        while(self.enemies_spawned < self.cap):
            r1 = random.randint(-self.range, self.range)
            r2 = random.randint(-self.range, self.range)
            spawn_pos = vec(r1,r2) + self.rect.center

            too_close = False
            for sprite in self.game.sprite_list:
                dist = spawn_pos - sprite.pos
                if abs(dist.length()) < SPAWNER_BUFFER:
                    too_close = True
                    break
            if not too_close:
                enemy = Enemy(self.game, (spawn_pos[0]), (spawn_pos[1]), ENEMY_HP)
                self.enemies_spawned += 1

            num_tries += 1
            if num_tries > SPAWN_ATTEMPTS:
                break

    def draw_health(self):
        if(self.hp > SPAWNER_HP * 0.6):
            color = GREEN
        elif self.hp > SPAWNER_HP * 0.3:
            color = YELLOW
        else:
            color = RED

        width = int(self.width * self.hp / SPAWNER_HP)
        self.health_bar = pg.Rect(0, 0, width, 7)
        self.health_bar.centerx, self.health_bar.centery = self.pos[0] + self.rect.width/2, self.pos[1] - self.rect.height
        self.health_bar.centerx += self.game.camera.x
        self.health_bar.centery += self.game.camera.y

        if self.hp < SPAWNER_HP:
            pg.draw.rect(self.game.screen, color, self.health_bar)

    def update(self):
        if self.hp <= 0:
            self.kill()

        self.count += 1
        start = False
        if self.count >= self.delay:
            if len(self.game.enemy_list) <= MAX_ENEMIES:
                start = True

        if start:
            if self.count > self.rate - len(self.game.spawner_blast):
                spawn_animation = Animation(self.game, self.rect.centerx, self.rect.centery, self.game.spawner_blast)
            if self.count > self.rate:
                self.count = 0
                self.spawn_enemies()