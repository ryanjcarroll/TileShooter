import pygame as pg
from math import atan2, degrees, cos, sin, sqrt
from settings import *
import random
from pygame import Vector2 as vec

##returns true if the given circle object and rectangle.rect are collided by at least a buffer amount
def circle_rect_collided(c, r, buffer):
    cx = c.pos.x
    cy = c.pos.y
    rx = r.x
    ry = r.y
    test_x = cx
    test_y = cy

    if (cx < rx):
        test_x = rx
    elif (cx > rx + r.width):
        test_x = rx + r.width

    if (cy < ry):
        test_y = ry
    elif (cy > ry + r.height):
        test_y = ry + r.height

    dist_x = cx - test_x
    dist_y = cy - test_y
    distance = sqrt(dist_x ** 2 + dist_y ** 2)
    if (distance <= (c.width / 2) + buffer):
        return True
    else:
        return False

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.layer = PLAYER_LAYER

        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.rot = 0

        self.game = game
        self.image = self.game.player_img
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.game = game
        self.rect.center = self.pos

        self.hitbox = PLAYER_HITBOX
        self.hp = PLAYER_HP
        self.hitbox.center = self.pos

        self.hit_vel = vec(0,0)
        self.hit_count = 0
        self.hit = False

    def move(self, vx, vy):
        self.vel = vec(vx,vy)
        self.pos += self.vel * self.game.dt

        ##undo if results in a wall collision
        if(self.wall_collision()):
            self.pos -= self.vel * self.game.dt

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def rotate(self):
        mouse_x = pg.mouse.get_pos()[0] - self.game.camera.camera.topleft[0]
        mouse_y = pg.mouse.get_pos()[1] - self.game.camera.camera.topleft[1]

        delta_x = mouse_x - self.pos[0]
        delta_y = mouse_y - self.pos[1]
        self.rot = -atan2(delta_y, delta_x)

        self.image = pg.transform.rotate(self.game.player_img, degrees(self.rot))
        self.rect = self.image.get_rect()

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def wall_collision(self):
        b = False
        for wall in self.game.wall_list:
            if(circle_rect_collided(self, wall.rect, -5)):
                b = True
                break
        for spawner in self.game.spawner_list:
            if (circle_rect_collided(self, spawner.hitbox, -7)):
                b = True
                break
        return b

    def check_keys(self):
        keys = pg.key.get_pressed()
        vel = PLAYER_SPEED
        if keys[pg.K_LSHIFT]:
            vel /= 4
        vx,vy = 0, 0

        if keys[pg.K_a] or keys[pg.K_LEFT]:
            vx = -vel
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            vx = vel
        if keys[pg.K_w] or keys[pg.K_UP]:
            vy = -vel
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            vy = vel

        if (abs(vx) > 0 and abs(vy) > 0):
            self.move(sqrt(2)*vx/2, 0)
            self.move(0, sqrt(2)*vy/2)
        else:
            self.move(vx, 0)
            self.move(0, vy)

    def update(self):
        if not self.hit:
            self.check_hit()
            self.rotate()
            self.check_keys()
        else:
            self.get_hit()

    def check_hit(self):
        for enemy in self.game.enemy_list:
            if circle_rect_collided(enemy, self.hitbox, -15):
                self.hit = True
                self.hp -= enemy.damage
                print(self.hp)
                self.hit_vel = enemy.vel
                enemy.vel = -enemy.vel

    def get_hit(self):
        ##animation for when the player is hit by an enemy
        if self.hit_count < PLAYER_HIT_TIME:
            self.hit_count += 1
            self.vel = self.hit_vel
            self.pos += self.vel * self.game.dt

            self.rot += 10
            self.image = pg.transform.rotate(self.game.player_img, self.rot)
            self.rect = self.image.get_rect()

            if (self.wall_collision()):
                self.pos -= self.vel * self.game.dt

            if (self.hit_count % 6 < 3):
                self.image = pg.transform.rotate(self.game.empty_player_img, degrees(self.rot))
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
                self.hitbox.center = self.pos

            self.rect.center = self.pos
            self.hitbox.center = self.pos
        elif self.hit_count < (PLAYER_HIT_TIME + PLAYER_RESPAWN_TIME):
            self.hit_count += 1

            self.check_keys()
            self.rotate()
            if (self.hit_count % 6 < 3):
                self.image = pg.transform.rotate(self.game.empty_player_img, degrees(self.rot))
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
                self.hitbox.center = self.pos
        else:
            self.hit = False
            self.hit_count = 0

    def shoot(self):
        angle = -self.rot

        bullet_x = self.pos.x + 10 * cos(angle + 0.55)
        bullet_y = self.pos.y + 10 * sin(angle + 0.55)
        bullet = Bullet(self.game, bullet_x, bullet_y, angle)

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y, angle):
        self.groups = game.bullet_list, game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.layer = BULLET_LAYER

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

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.wall_list, game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.layer = WALL_LAYER

        self.game = game
        self.image = self.game.wall_img
        self.rect = self.image.get_rect()

        self.pos = vec(x + TILE_SIZE/2, y + TILE_SIZE/2)
        self.rect.center = self.pos

class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.layer = WALL_LAYER

        self.game = game
        self.image = self.game.floor_img
        self.rect = self.image.get_rect()

        self.pos = vec(x + TILE_SIZE / 2, y + TILE_SIZE / 2)
        self.rect.center = self.pos

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, hp):
        self.groups = game.enemy_list, game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.layer = ENEMY_LAYER

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
                    self.animation = self.game.enemy_move
                bullet.kill()
                self.hp -= bullet.damage
                if(self.hp < 1):
                    self.kill()

    def update(self):
        if(self.animation_count < len(self.animation) - 1):
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

class Spawner(pg.sprite.Sprite):
    def __init__(self, game, x, y, rate, cap, range, hp, delay):
        self.groups = game.spawner_list, game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.layer = WALL_LAYER
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

        while(self.enemies_spawned < self.cap):
            spawn_pos = vec(random.randint(-self.range, self.range), random.randint(-self.range, self.range))

            too_close = False
            for sprite in self.game.sprite_list:
                dist = sprite.pos - spawn_pos
                if(abs(dist.length()) < sprite.rect.width + self.width):
                    too_close = True

            if not too_close:
                enemy = Enemy(self.game, (self.pos[0] + spawn_pos[0]), (self.pos[1] + spawn_pos[1]), ENEMY_HP)
                self.enemies_spawned += 1

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
            start = True

        if start:
            if self.count > self.rate:
                self.count = 0
                self.spawn_enemies()

