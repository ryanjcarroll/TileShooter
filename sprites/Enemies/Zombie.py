from sprites.Enemies.Enemy import Enemy
import pygame as pg
from pygame import Vector2 as vec
from settings import *

class Zombie(Enemy):
    def __init__(self, game, x:int, y:int):
        """
        Initialize a Zombie enemy.
        """
        # initialize a generic enemy first.
        super().__init__(game, x, y)

        # set image
        self.image = pg.transform.rotate(self.game.zombie_img, self.rot)
        self.rect = self.image.get_rect()
        self.width = self.rect.width

        # set attributes
        self.speed = ZOMBIE_SPEED
        self.damage = ZOMBIE_DAMAGE

        self.max_hp = ZOMBIE_HP
        self.hp = ZOMBIE_HP
        self.hitbox = ZOMBIE_HITBOX
        self.hitbox.center = self.pos

    def load_animations(self):
        # set spritelists for animations
        self.move_animation = [pg.image.load(f"images/{i}.png") for i in range(2,27,1)]
        self.idle_animation = [pg.image.load("images/2.png")]
        self.animation = self.idle_animation

    def move(self):
        """
        Called each game step, handles enemy movement patterns.
        """
        # rotate to face the player
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.animation[self.animation_count], self.rot)
        self.rect = self.image.get_rect()

        # accelerate toward the player, avoiding enemies and walls
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_enemies()
        self.avoid_walls()
        if self.acc.length() > 0:
            self.acc.scale_to_length(self.speed)
        self.acc -= 2 * self.vel
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt**2

        # if wall collision, bounce off the wall by a set amount
        if self.wall_collision():
            self.pos -= self.vel * self.game.dt + 0.5 * self.acc * self.game.dt**2
            self.vel *= -WALL_BOUNCE

        self.rect.center = self.pos
        self.hitbox.center = self.pos