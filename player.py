from settings import *
import pygame as pg
import math
from game_types import GameType


class Player:
    def __init__(self, game: GameType):
        self.game = game
        self.x, self.y = PLAYER_POSITION
        self.angle = PLAYER_ANGLE

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        delta_x, delta_y = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            delta_x += speed_cos
            delta_y += speed_sin
        if keys[pg.K_s]:
            delta_x += -speed_cos
            delta_y += -speed_sin
        if keys[pg.K_a]:
            delta_x += speed_sin
            delta_y += -speed_cos
        if keys[pg.K_d]:
            delta_x += -speed_sin
            delta_y += speed_cos

        self.check_wall_collision(delta_x, delta_y)

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROTATION_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROTATION_SPEED * self.game.delta_time

        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, delta_x, delta_y):
        if self.check_wall(int(self.x + delta_x), int(self.y)):
            self.x += delta_x
        if self.check_wall(int(self.x), int(self.y + delta_y)):
            self.y += delta_y

    def draw(self):
        # pg.draw.line(
        #     self.game.screen,
        #     "yellow",
        #     (self.x * 100, self.y * 100),
        #     (
        #         self.x * 100 + WIDTH * math.cos(self.angle),
        #         self.y * 100 + WIDTH * math.sin(self.angle),
        #     ),
        #     2,
        # )

        pg.draw.circle(self.game.screen, "green", (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()

    @property
    def position(self):
        return (self.x, self.y)

    @property
    def map_position(self):
        return int(self.x), int(self.y)
