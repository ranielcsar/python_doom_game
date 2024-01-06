from settings import *
import pygame as pg
import math
from game_types import GameType


class Player:
    def __init__(self, game: GameType):
        self.game = game
        self.x, self.y = PLAYER_POSITION
        self.angle = PLAYER_ANGLE
        self.relative_movement = 0
        self.shot = False

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

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

        self.angle %= math.tau  # 2 pi

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, delta_x, delta_y):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time

        if self.check_wall(int(self.x + delta_x * scale), int(self.y)):
            self.x += delta_x
        if self.check_wall(int(self.x), int(self.y + delta_y * scale)):
            self.y += delta_y

    def mouse_control(self):
        mouse_x, mouse_y = pg.mouse.get_pos()

        if mouse_x < MOUSE_BORDER_LEFT or mouse_x > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])

        self.relative_movement = pg.mouse.get_rel()[0]
        self.relative_movement = max(
            -MOUSE_MAX_RELATIVE_MOVEMENT,
            min(MOUSE_MAX_RELATIVE_MOVEMENT, self.relative_movement),
        )
        self.angle += self.relative_movement * MOUSE_SENSITIVITY * self.game.delta_time

    def draw(self):
        # pg.draw.line(
        #     self.game.screen,
        #     "yellow",
        #     (self.x * PIXEL_SIZE, self.y * PIXEL_SIZE),
        #     (
        #         self.x * PIXEL_SIZE + WIDTH * math.cos(self.angle),
        #         self.y * PIXEL_SIZE + WIDTH * math.sin(self.angle),
        #     ),
        #     2,
        # )

        pg.draw.circle(
            self.game.screen, "green", (self.x * PIXEL_SIZE, self.y * PIXEL_SIZE), 15
        )

    def update(self):
        self.movement()
        self.mouse_control()

    @property
    def position(self):
        return (self.x, self.y)

    @property
    def map_position(self):
        return int(self.x), int(self.y)
