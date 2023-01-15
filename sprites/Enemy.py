import pygame as pg
from settings import *
from ._utility import *
from pygame import Vector2 as vec
import random

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, hp):
        self.groups = game.enemy_list, game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        game.sprite_list.change_layer(self, ENEMY_LAYER)

        self.game = game
        self.rot = random.randint(0,360)
        self.image = pg.transform.rotate(self.game.enemy_img, self.rot)
        self.rect = self.image.get_rect()
        self.width = self.rect.width

        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.avoid_wall = vec(0,0)
        self.avoid_enemy = vec(0,0)
        self.hp = hp
        self.chase = False
        self.speed = ENEMY_SPEED

        self.damage = ENEMY_DAMAGE
        self.hitbox = ENEMY_HITBOX
        self.hitbox.center = self.pos

        self.wait_count = 0
        self.animation = self.game.enemy_idle
        self.animation_count = 0

    def move(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.animation[self.animation_count], self.rot)
        self.rect = self.image.get_rect()

        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_enemies()
        self.avoid_walls()
        if self.acc.length() > 0:
            self.acc.scale_to_length(self.speed)
        self.acc -= 2*self.vel
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

        if(self.wall_collision()):
            self.pos -= self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.vel *= -WALL_BOUNCE

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def wall_collision(self):
        b = False
        for wall in self.game.wall_list:
            if (circle_rect_collided(self, wall.rect, -7)):
                b = True
                break
        return b

    def avoid_walls(self):
        for wall in self.game.wall_list:
            to_wall = self.pos - wall.pos
            if 0 < to_wall.length() < AVOID_WALLS_RADIUS:
                self.acc += to_wall.normalize() * AVOID_WALLS_WEIGHT

    def avoid_enemies(self):
        for enemy in self.game.enemy_list:
            if(enemy != self):
                to_enemy = self.pos - enemy.pos
                if 0 < to_enemy.length() < AVOID_ENEMIES_RADIUS:
                    self.acc += to_enemy.normalize() * AVOID_ENEMIES_WEIGHT

    def hit(self):
        for bullet in self.game.bullet_list:
            if pg.sprite.collide_rect(self, bullet):
                self.vel += bullet.vel * KNOCKBACK
                if(self.chase == False):
                    self.chase = True
                    self.wait_count = ENEMY_WAIT
                    self.animation = self.game.enemy_move
                bullet.kill()
                self.hp -= bullet.damage
                if(self.hp < 1):
                    self.kill()

    def draw_health(self):
        if (self.hp > ENEMY_HP * 0.6):
            color = GREEN
        elif self.hp > ENEMY_HP * 0.3:
            color = YELLOW
        else:
            color = RED

        width = int(self.width * self.hp / ENEMY_HP)
        self.health_bar = pg.Rect(0, 0, width, 7)
        self.health_bar.centerx, self.health_bar.centery = self.pos[0], self.pos[
            1] - self.rect.height/2
        self.health_bar.centerx += self.game.camera.x
        self.health_bar.centery += self.game.camera.y

        if self.hp < ENEMY_HP:
            pg.draw.rect(self.game.screen, color, self.health_bar)

    def update(self):
        if(self.wait_count < ENEMY_WAIT):
            self.image = pg.transform.rotate(self.animation[self.animation_count], self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hitbox.center = self.pos

            self.hit()
            self.wait_count += 1
        else:
            if (self.animation_count < len(self.animation) - 1):
                self.animation_count += 1
            else:
                self.animation_count = 0
            self.image = pg.transform.rotate(self.animation[self.animation_count], self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

            if ((self.chase == False) and ((self.game.player.pos - self.pos).length() < AGGRO_RADIUS)):
                self.chase = True
                self.animation = self.game.enemy_move

            if self.chase:
                self.move()

            self.hit()
            self.rect.center = self.pos