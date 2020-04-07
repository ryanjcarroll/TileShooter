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

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)

        self.pos = vec(x,y)
        self.vel = vec(0,0)

        self.image = pg.image.load("images/circle.png")
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.game = game

        self.rect.center = self.pos

    def move(self, vx, vy):
        self.vel = vec(vx,vy)
        self.pos += self.vel * self.game.dt

        ##undo if results in a wall collision
        if(self.wall_collision()):
            self.pos -= self.vel * self.game.dt

        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def rotate(self):
        player_x, player_y = self.pos
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

        self.pos = vec(x,y)
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

        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

        self.pos = vec(x,y)
        self.vel = vec(0,0)

        self.avoid_wall = vec(0,0)
        self.avoid_enemy = vec(0,0)
        self.hp = hp
        self.chase = False

    def move(self):
        vec_to_player = self.game.player.pos - self.pos

        if(vec_to_player.length() > 0):
            self.vel = vec_to_player.normalize()

        self.vel += self.avoid_walls() * AVOID_WALLS_WEIGHT
        self.vel += self.avoid_enemies() * AVOID_ENEMIES_WEIGHT

        self.vel = self.vel.normalize() * ENEMY_SPEED
        self.pos += self.vel * self.game.dt

        if(self.wall_collision()):
            self.pos += -self.vel * self.game.dt

    def wall_collision(self):
        for wall in self.game.wall_list:
            if pg.sprite.collide_rect(self, wall):
                return True
                break
        return False

    def avoid_walls(self):
        avoid_wall = vec(0,0)
        for wall in self.game.wall_list:
            to_wall = self.pos - wall.pos
            if 0 < to_wall.length() < AVOID_WALLS_RADIUS:
                avoid_wall += (to_wall.normalize() * (AVOID_WALLS_RADIUS - to_wall.length()))
        return avoid_wall

    def avoid_enemies(self):
        avoid_enemy = vec(0,0)
        for enemy in self.game.enemy_list:
            if(enemy != self):
                to_enemy = enemy.pos - self.pos
                if 0 < to_enemy.length() < AVOID_ENEMIES_RADIUS:
                    avoid_enemy += (to_enemy.normalize() * (AVOID_ENEMIES_RADIUS - to_enemy.length()**2))
        return avoid_enemy

    def hit(self):
        for bullet in self.game.bullet_list:
            if pg.sprite.collide_rect(self, bullet):
                if(self.chase == False):
                    self.chase = True
                bullet.kill()
                self.hp -= 1
                if(self.hp < 3):
                    self.image.fill(RED)
                    if(self.hp < 1):
                        self.kill()

    def update(self):
        if (self.game.player.pos - self.pos).length() < 256:
            self.chase = True
        if(self.chase):
            self.move()

        self.hit()
        self.rect.center = self.pos
