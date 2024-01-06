from sprite_object import *
from npc import *


class ObjectHandler:
    def __init__(self, game: GameType):
        self.game = game
        self.sprite_list: list[SpriteObject] = []
        self.npc_list: list[NPC] = []
        self.npc_sprite_path = "resources/sprites/npc/"
        self.static_sprite_path = "resources/sprites/static_sprites/"
        self.animated_sprite_path = "resources/sprites/animated_sprites/"
        add_sprite = self.add_sprite
        add_npc = self.add_npc

        # sprites
        add_sprite(AnimatedSprite(game))
        add_sprite(SpriteObject(game))

        # npc
        add_npc(NPC(game))

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def update(self):
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
