import pygame as pg
from game_types import GameType


class Sound:
    def __init__(self, game: GameType):
        self.game = game
        pg.mixer.init()
        self.path = "resources/sound"
        self.shotgun = pg.mixer.Sound(f"{self.path}/shotgun.wav")
        self.npc_pain = pg.mixer.Sound(f"{self.path}/npc_pain.wav")
        self.npc_death = pg.mixer.Sound(f"{self.path}/npc_death.wav")
        self.npc_attack = pg.mixer.Sound(f"{self.path}/npc_attack.wav")
        self.player_pain = pg.mixer.Sound(f"{self.path}/player_pain.wav")
        self.theme = pg.mixer.Sound(f"{self.path}/theme.mp3")
