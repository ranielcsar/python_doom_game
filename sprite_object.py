import pygame as pg
from settings import *
from game_types import GameType
import math
import os
from collections import deque


class SpriteObject:
    def __init__(
        self,
        game: GameType,
        path="resources/sprites/static_sprites/candlebra.png",
        position=(10.5, 3.5),
        scale=0.7,
        shift=0.27,
    ):
        self.game = game
        self.player = game.player
        self.x, self.y = position
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.IMAGE_WIDTH // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        (
            self.delta_x,
            self.delta_y,
            self.theta,
            self.screen_x,
            self.distance,
            self.normal_distance,
        ) = (0, 0, 0, 0, 1, 1)
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        projection = SCREEN_DISTANCE / self.normal_distance * self.SPRITE_SCALE
        projection_width, projection_height = projection * self.IMAGE_RATIO, projection

        image = pg.transform.scale(self.image, (projection_width, projection_height))

        self.sprite_half_width = projection_width // 2
        height_shift = projection_height * self.SPRITE_HEIGHT_SHIFT
        position = (
            self.screen_x - self.sprite_half_width,
            HALF_HEIGHT - projection_height // 2 + height_shift,
        )

        self.game.raycasting.objects_to_render.append(
            (self.normal_distance, image, position)
        )

    def get_sprites(self):
        delta_x = self.x - self.player.x
        delta_y = self.y - self.player.y
        self.delta_x, self.delta_y = delta_x, delta_y
        self.theta = math.atan2(delta_y, delta_x)

        delta = self.theta - self.player.angle
        if (delta_x > 0 and self.player.angle > math.pi) or (
            delta_x < 0 and delta_y < 0
        ):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.distance = math.hypot(delta_x, delta_y)
        self.normal_distance = self.distance * math.cos(delta)

        if (
            -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH)
            and self.normal_distance > 0.5
        ):
            self.get_sprite_projection()

    def update(self):
        self.get_sprites()


class AnimatedSprite(SpriteObject):
    def __init__(
        self,
        game: GameType,
        path="resources/sprites/animated_sprites/green_light/0.png",
        position=(11.5, 3.5),
        scale=0.7,
        shift=0.27,
        animation_time=120,
    ):
        super().__init__(game, path, position, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit("/", 1)[0]
        self.images = self.get_images(self.path)
        self.previous_animation_time = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()

        if time_now - self.previous_animation_time > self.animation_time:
            self.previous_animation_time = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()

        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                image = pg.image.load(path + "/" + file_name).convert_alpha()
                images.append(image)

        return images
