import pygame as pg
import math
from settings import *
from game_types import GameType, ObjectsToRenderType, RayCastResultType


class RayCasting:
    def __init__(self, game: GameType):
        self.game = game
        self.ray_casting_result: RayCastResultType = []
        self.objects_to_render: ObjectsToRenderType = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []

        for ray, values in enumerate(self.ray_casting_result):
            depth, projection_height, texture, offset = values

            if projection_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(
                    wall_column, (SCALE, projection_height)
                )
                wall_position = (ray * SCALE, HALF_HEIGHT - projection_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / projection_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE),
                    HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE,
                    texture_height,
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_position = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_position))

    def ray_cast(self):
        self.ray_casting_result = []
        player_x_pos, player_y_pos = self.game.player.position
        player_x_map, player_y_map = self.game.player.map_position

        texture_horizontal, texture_vertical = 1, 1

        ray_angle = self.game.player.angle - HALF_FIELD_OF_VIEW + 0.0001
        for _ in range(NUM_RAYS):
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
                    texture_horizontal = self.game.map.world_map[vertical_block]
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
                    texture_vertical = self.game.map.world_map[vertical_block]
                    break

                v_intersection_coord_x += delta_x
                v_intersection_coord_y += delta_y
                v_depth += delta_depth

            # depth, texture offset
            if v_depth < h_depth:
                depth, texture = v_depth, texture_vertical
                v_intersection_coord_y %= 1
                offset = (
                    v_intersection_coord_y
                    if cos_a > 0
                    else (1 - v_intersection_coord_y)
                )
            else:
                depth, texture = h_depth, texture_horizontal
                h_intersection_coord_x %= 1
                offset = (
                    (1 - h_intersection_coord_x)
                    if sin_a > 0
                    else h_intersection_coord_x
                )

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            projection_height = SCREEN_DISTANCE / (depth + 0.0001)

            # ray casting result
            self.ray_casting_result.append((depth, projection_height, texture, offset))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()
