from settings import *
import pygame as pg
import math
from game_types import GameType


class Player:
    def __init__(self, game: GameType):
        self.game = game
        self.x, self.y = PLAYER_POSITION
        self.angle = PLAYER_ANGLE
        self.relative_mouse_movement = 0
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.health_recovery_delay = 700
        self.previous_time = pg.time.get_ticks()

    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()

        if time_now - self.previous_time > self.health_recovery_delay:
            self.previous_time = time_now
            return True

    def check_game_over(self):
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def get_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()

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
        mouse_x, _ = pg.mouse.get_pos()

        if mouse_x < MOUSE_BORDER_LEFT or mouse_x > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])

        self.relative_mouse_movement = pg.mouse.get_rel()[0]
        self.relative_mouse_movement = max(
            -MOUSE_MAX_RELATIVE_MOVEMENT,
            min(MOUSE_MAX_RELATIVE_MOVEMENT, self.relative_mouse_movement),
        )
        self.angle += (
            self.relative_mouse_movement * MOUSE_SENSITIVITY * self.game.delta_time
        )

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
        self.recover_health()

    @property
    def position(self):
        return (self.x, self.y)

    @property
    def map_position(self):
        return (int(self.x), int(self.y))
