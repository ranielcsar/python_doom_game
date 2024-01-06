from sprite_object import *
from random import randint, random, choice
import pygame as pg


class NPC(AnimatedSprite):
    def __init__(
        self,
        game: GameType,
        path="resources/sprites/npc/soldier/0.png",
        position=(10.5, 5.5),
        scale=0.6,
        shift=0.38,
        animation_time=180,
    ):
        super().__init__(game, path, position, scale, shift, animation_time)

        self.attack_images = self.get_images(self.path + "/attack")
        self.death_images = self.get_images(self.path + "/death")
        self.idle_images = self.get_images(self.path + "/idle")
        self.pain_images = self.get_images(self.path + "/pain")
        self.walk_images = self.get_images(self.path + "/walk")

        self.attack_distance = randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0

    def update(self):
        self.check_animation_time()
        self.get_sprites()
        self.run_logic()
        # self.draw_ray_cast()

    def animate_death(self):
        if not self.alive:
            if (
                self.game.global_trigger
                and self.frame_counter < len(self.death_images) - 1
            ):
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_pain(self):
        self.animate(self.pain_images)

        if self.animation_trigger:
            self.pain = False

    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if (
                HALF_WIDTH - self.sprite_half_width
                < self.screen_x
                < HALF_WIDTH + self.sprite_half_width
            ):
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npc_death.play()

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_hit_in_npc()

            if self.pain:
                self.animate_pain()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    @property
    def map_position(self):
        return (int(self.x), int(self.y))

    def ray_cast_player_npc(self):
        if self.game.player.position == self.map_position:
            return True

        wall_distance_vertical, wall_distance_horizontal = 0, 0
        player_distance_vertical, player_distance_horizontal = 0, 0

        player_x_pos, player_y_pos = self.game.player.position
        player_x_map, player_y_map = self.game.player.map_position

        ray_angle = self.theta

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
            vertical_block = int(h_intersection_coord_x), int(h_intersection_coord_y)

            if vertical_block == self.map_position:
                player_distance_horizontal = h_depth
                break
            if vertical_block in self.game.map.world_map:
                wall_distance_horizontal = h_depth
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
            vertical_block = int(v_intersection_coord_x), int(v_intersection_coord_y)

            if vertical_block == self.map_position:
                player_distance_vertical = v_depth
                break
            if vertical_block in self.game.map.world_map:
                wall_distance_vertical = v_depth
                break

            v_intersection_coord_x += delta_x
            v_intersection_coord_y += delta_y
            v_depth += delta_depth

        player_distance = max(player_distance_horizontal, player_distance_vertical)
        wall_distance = max(wall_distance_horizontal, wall_distance_vertical)

        if 0 < player_distance < wall_distance or not wall_distance:
            return True
        return False

    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, "red", (100 * self.x, 100 * self.y), 15)

        if self.ray_cast_player_npc():
            pg.draw.line(
                self.game.screen,
                "orange",
                (100 * self.game.player.x, 100 * self.game.player.y),
                (100 * self.x, 100 * self.y),
                2,
            )