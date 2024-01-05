import pygame as pg
from game_types import GameType


class Sound:
    def __init__(self, game: GameType):
        self.game = game
        pg.mixer.init()
        self.path = "resources/sound"
        self.shotgun = pg.mixer.Sound(f"{self.path}/shotgun.wav")
