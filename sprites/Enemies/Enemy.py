import pygame as pg
from settings import *
from .._utility import *
from pygame import Vector2 as vec
import random
from abc import abstractmethod


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x:int, y:int):
        """
        Initialize an enemy with set attributes.
        """
        # add to game groups and sprite lists
        self.groups = [game.enemy_list, game.sprite_list]
        pg.sprite.Sprite.__init__(self, self.groups)
        game.sprite_list.change_layer(self, ENEMY_LAYER)
        self.game = game

        # load animation assets
        self.load_animations()

        # starting movement and position vectors
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = random.randint(0, 360)
        self.avoid_wall = vec(0, 0)
        self.avoid_enemy = vec(0, 0)
        self.chase = False

        # start timers/counters
        self.wait_count = 0
        self.animation_count = 0


    @abstractmethod
    def load_animations(self):
        # set spritelists for animations
        self.move_animation = [pg.image.load(f"images/circle.png")]
        self.idle_animation = [pg.image.load(f"images/circle.png")]
        self.animation = self.idle_animation

    @abstractmethod
    def move(self):
        """
        Called each game step, handles enemy movement patterns.
        """
        ...
       

    def wall_collision(self):
        """
        Check for wall collisions.
        """
        b = False
        for wall in self.game.wall_list:
            if circle_rect_collided(self, wall.rect, -7):
                b = True
                break
        return b

    def avoid_walls(self):
        """
        Add a movement vector away from nearby walls.
        """
        for wall in self.game.wall_list:
            to_wall = self.pos - wall.pos
            if 0 < to_wall.length() < AVOID_WALLS_RADIUS:
                self.acc += to_wall.normalize() * AVOID_WALLS_WEIGHT

    def avoid_enemies(self):
        """
        Add a movement vector away from other nearby enemies.
        """
        for enemy in self.game.enemy_list:
            if enemy != self:
                to_enemy = self.pos - enemy.pos
                if 0 < to_enemy.length() < AVOID_ENEMIES_RADIUS:
                    self.acc += to_enemy.normalize() * AVOID_ENEMIES_WEIGHT

    def hit(self):
        """
        Reveice a knockback when hit by bullets.
        """
        for bullet in self.game.bullet_list:
            if pg.sprite.collide_rect(self, bullet):
                self.vel += bullet.vel * KNOCKBACK
                if self.chase == False:
                    self.chase = True
                    self.wait_count = ENEMY_WAIT
                    self.animation = self.move_animation
                bullet.kill()
                self.hp -= bullet.damage
                if self.hp < 1:
                    self.kill()

    def draw_health(self):
        """
        Draw healthbar over the enemy sprite.
        """
        if self.hp > self.max_hp * 0.6:
            color = GREEN
        elif self.hp > self.max_hp * 0.3:
            color = YELLOW
        else:
            color = RED

        width = int(self.width * self.hp / self.max_hp)
        self.health_bar = pg.Rect(0, 0, width, 7)
        self.health_bar.centerx, self.health_bar.centery = (
            self.pos[0],
            self.pos[1] - self.rect.height / 2,
        )
        self.health_bar.centerx += self.game.camera.x
        self.health_bar.centery += self.game.camera.y

        if self.hp < self.max_hp:
            pg.draw.rect(self.game.screen, color, self.health_bar)

    def update(self):
        """
        Update the image and hitbox after movements. If animations exist, take the next step through the animation cycle. Register hits and movements.
        """
        if self.wait_count < ENEMY_WAIT:
            self.image = pg.transform.rotate(
                self.animation[self.animation_count], self.rot
            )
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hitbox.center = self.pos

            self.hit()
            self.wait_count += 1
        else:
            if self.animation_count < len(self.animation) - 1:
                self.animation_count += 1
            else:
                self.animation_count = 0
            self.image = pg.transform.rotate(
                self.animation[self.animation_count], self.rot
            )
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

            if (self.chase == False) and (
                (self.game.player.pos - self.pos).length() < AGGRO_RADIUS
            ):
                self.chase = True
                self.animation = self.move_animation
            if self.chase:
                self.move()

            self.hit()
            self.rect.center = self.pos
