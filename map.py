import pygame as pg
from game_types import GameType, MiniMapType, WorldMapType
from settings import PIXEL_SIZE

_ = False
mini_map = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, 2, 2, 2, 2, _, _, _, 1, 1, 1, _, _, 3],
    [3, _, _, _, _, _, 4, _, _, _, _, _, 1, _, _, 4],
    [3, _, _, _, _, _, 4, _, _, _, _, _, 1, _, _, 4],
    [3, _, _, 2, 2, 2, 2, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, 3, _, _, _, 3, _, _, _, _, _, _, _, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3],
]


class Map:
    def __init__(self, game: GameType):
        self.game = game
        self.mini_map: MiniMapType = mini_map
        self.world_map: WorldMapType = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [
            pg.draw.rect(
                self.game.screen,
                "darkgray",
                (
                    position[0] * PIXEL_SIZE,
                    position[1] * PIXEL_SIZE,
                    PIXEL_SIZE,
                    PIXEL_SIZE,
                ),
                2,
            )
            for position in self.world_map
        ]
