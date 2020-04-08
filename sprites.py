import pygame as pg
from math import atan2, degrees, cos, sin, sqrt
from settings import *
import random
from pygame import Vector2 as vec

##returns true if the given circle and rectangle are collided
def circle_rect_collided(c, r):
    cx = c.pos.x
    cy = c.pos.y
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

def collide_hit_rect(one, two):
    return one.hitbox.colliderect(two.rect)

def wall_collide(sprite, group, dir):
    if dir == 'x':
        walls_hit = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if walls_hit:
            if walls_hit[0].rect.centerx > sprite.hitbox.centerx:
                sprite.pos.x = walls_hit[0].rect.left - sprite.hitbox.width / 2
            if walls_hit[0].rect.centerx < sprite.hitbox.centerx:
                sprite.pos.x = walls_hit[0].rect.right + sprite.hitbox.width / 2
            sprite.vel.x = 0
            sprite.hitbox.centerx = sprite.pos.x

    if dir == 'y':
        walls_hit = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if walls_hit:
            if walls_hit[0].rect.centery > sprite.hitbox.centery:
                sprite.pos.y = walls_hit[0].rect.top - sprite.hitbox.height / 2
            if walls_hit[0].rect.centery < sprite.hitbox.centery:
                sprite.pos.y = walls_hit[0].rect.bottom + sprite.hitbox.height / 2
            sprite.vel.y = 0
            sprite.hitbox.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)

        self.pos = vec(x,y)
        self.vel = vec(0,0)

        self.game = game
        self.image = self.game.player_img
        self.rect = self.image.get_rect()
        self.hitbox = PLAYER_HITBOX
        self.width = self.rect.width
        self.game = game

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def move(self, vx, vy):
        self.vel = vec(vx,vy)
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt

        ##undo if results in a wall collision
        if(self.wall_collision()):
            self.pos -= self.vel * self.game.dt

        self.hitbox.centerx = self.pos.x
        wall_collide(self, self.game.wall_list, 'x')
        self.hitbox.centery = self.pos.y
        wall_collide(self, self.game.wall_list, 'y')
        self.rect.center = self.hitbox.center

    def rotate(self):
        player_x, player_y = self.pos
        mouse_x, mouse_y = pg.mouse.get_pos()

        delta_x = mouse_x - player_x
        delta_y = mouse_y - player_y
        angle = -atan2(delta_y, delta_x)

        deg = degrees(angle)

        new_image = self.game.player_img
        rotated_image = pg.transform.rotate(new_image, deg)
        new_rect = rotated_image.get_rect()

        self.image = rotated_image
        self.rect = new_rect

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def wall_collision(self):
        b = False
        for wall in self.game.wall_list:
            if(circle_rect_collided(self, wall)):
                b = True
                break
        return b

    def check_keys(self):
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

    def wait_random(self):
        ##tester method for framerate variations
        ran = random.randint(0,100)
        pg.time.delay(ran)

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

    def out_of_bounds(self):
        if(self.pos.x < 0 or self.pos.y < 0 or self.pos.x > WIDTH or self.pos.y > HEIGHT):
            self.kill()
        if (self.pos - self.orig_pos).length() > BULLET_RANGE:
            self.kill()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
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

        self.pos = vec(x + TILE_SIZE/2, y + TILE_SIZE/2)
        self.rect.center = self.pos

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, hp):
        self.groups = game.enemy_list, game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.rot = random.randint(0,360)
        self.image = pg.transform.rotate(self.game.enemy_img, self.rot)
        self.rect = self.image.get_rect()
        self.hitbox = ENEMY_HITBOX
        self.width = self.rect.width

        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.center = self.pos
        self.hitbox.center = self.pos

        self.avoid_wall = vec(0,0)
        self.avoid_enemy = vec(0,0)
        self.hp = hp
        self.chase = False
        self.speed = ENEMY_SPEED

    def move(self):
        old_pos = self.pos
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.enemy_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_enemies()
        self.avoid_walls()
        if self.acc.length() > 0:
            self.acc.scale_to_length(self.speed)
        self.acc -= 2*self.vel
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

        self.hitbox.centerx = self.pos.x
        wall_collide(self, self.game.wall_list, 'x')
        self.hitbox.centery = self.pos.y
        wall_collide(self, self.game.wall_list, 'y')
        self.rect.center = self.hitbox.center

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
                bullet.kill()
                self.hp -= bullet.damage
                if(self.hp < 1):
                    self.kill()

    def update(self):
        if (self.game.player.pos - self.pos).length() < AGGRO_RADIUS:
            self.chase = True
        if(self.chase):
            self.move()

        self.hit()
        self.rect.center = self.pos