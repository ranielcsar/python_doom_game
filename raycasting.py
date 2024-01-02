import pygame as pg
import math
from settings import *
from game_types import GameType


class RayCasting:
    def __init__(self, game: GameType):
        self.game = game

    def ray_cast(self):
        player_x_pos, player_y_pos = self.game.player.position
        player_x_map, player_y_map = self.game.player.map_position

        ray_angle = self.game.player.angle - HALF_FIELD_OF_VIEW + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            h_intersection_coord_y, delta_y = (
                (player_y_map + 1, 1) if sin_a > 0 else (player_y_map - 1e-6, -1)
            )

            h_depth = (h_intersection_coord_y - player_y_pos) / sin_a
            h_intersection_coord_x = player_x_pos + h_depth * cos_a

            delta_depth = delta_y / sin_a
            delta_x = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                vertical_block = int(h_intersection_coord_x), int(
                    h_intersection_coord_y
                )
                if vertical_block in self.game.map.world_map:
                    break

                h_intersection_coord_x += delta_x
                h_intersection_coord_y += delta_y
                h_depth += delta_depth

            # verticals
            v_intersection_coord_x, delta_x = (
                (player_x_map + 1, 1) if cos_a > 0 else (player_x_map - 1e-6, -1)
            )

            v_depth = (v_intersection_coord_x - player_x_pos) / cos_a
            v_intersection_coord_y = player_y_pos + v_depth * sin_a

            delta_depth = delta_x / cos_a
            delta_y = sin_a * delta_depth

            for i in range(MAX_DEPTH):
                vertical_block = int(v_intersection_coord_x), int(
                    v_intersection_coord_y
                )
                if vertical_block in self.game.map.world_map:
                    break

                v_intersection_coord_x += delta_x
                v_intersection_coord_y += delta_y
                v_depth += delta_depth

            # depth
            depth = min(v_depth, h_depth)

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            projection_height = SCREEN_DISTANCE / (depth + 0.0001)

            # draw walls
            color = [255 / (1 + depth**5 * 0.00002)] * 3
            pg.draw.rect(
                self.game.screen,
                color,
                (
                    ray * SCALE,
                    HALF_HEIGHT - projection_height // 2,
                    SCALE,
                    projection_height,
                ),
            )

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
