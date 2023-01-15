import pygame as pg
from math import atan2, degrees, cos, sin, sqrt
from settings import *
from _utility import *
from pygame import Vector2 as vec
import Bullet

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.sprite_list
        pg.sprite.Sprite.__init__(self, self.groups)
        game.sprite_list.change_layer(self, PLAYER_LAYER)

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
        self.hitbox.center = self.pos

        self.hp = PLAYER_HP
        self.stamina = PLAYER_STAMINA

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
            vel *= 1.5
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

    def draw_health(self):
        if self.hp > PLAYER_HP * 0.6:
            color = GREEN
        elif self.hp > PLAYER_HP * 0.3:
            color = YELLOW
        else:
            color = RED

        width = int(PLAYER_HEALTHBAR_SIZE * self.hp / PLAYER_HP)
        self.health_bar = pg.Rect(0, 0, width, 20)
        self.health_bar.bottomleft = [32, (HEIGHT-32)]

        pg.draw.rect(self.game.screen, color, self.health_bar)

    def draw_stamina(self):
        color = ORANGE

        width = int(PLAYER_HEALTHBAR_SIZE * self.stamina / PLAYER_STAMINA)
        self.stamina_bar = pg.Rect(0, 0, width, 10)
        self.stamina_bar.bottomleft = [32, (HEIGHT-54)]

        pg.draw.rect(self.game.screen, color, self.stamina_bar)

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

    def update(self):
        if self.hp <= 0:
            self.game.playing = False
        if not self.hit:
            self.check_hit()
            self.rotate()
            self.check_keys()
        else:
            self.get_hit()