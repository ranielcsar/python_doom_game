import pygame as pg
from settings import *
from game_types import GameType


class ObjectRenderer:
    def __init__(self, game: GameType):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture(
            "resources/textures/sky.png", (WIDTH, HALF_HEIGHT)
        )
        self.sky_offset = 0
        self.blood_screen = self.get_texture(
            "resources/textures/blood_screen.png", RESOLUTION
        )
        digits_len = 11
        self.health_digit_size = 90
        self.health_digit_images = [
            self.get_texture(
                f"resources/textures/digits/{i}.png", [self.health_digit_size] * 2
            )
            for i in range(digits_len)
        ]
        self.health_digits = dict(
            zip(map(str, range(digits_len)), self.health_digit_images)
        )
        self.game_over_image = self.get_texture(
            "resources/textures/game_over.png", RESOLUTION
        )

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)

        for i, char in enumerate(health):
            self.screen.blit(
                self.health_digits[char],
                (i * self.health_digit_size, 0),
            )
        self.screen.blit(
            self.health_digits["10"], ((i + 1) * self.health_digit_size, 0)
        )

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (
            self.sky_offset + 4.0 * self.game.player.relative_movement
        ) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))

        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        objects_list = sorted(
            self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True
        )

        for depth, image, position in objects_list:
            self.screen.blit(image, position)

    @staticmethod
    def get_texture(path: str, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture("resources/textures/1.png"),
            2: self.get_texture("resources/textures/2.png"),
            3: self.get_texture("resources/textures/3.png"),
            4: self.get_texture("resources/textures/4.png"),
            5: self.get_texture("resources/textures/5.png"),
        }
