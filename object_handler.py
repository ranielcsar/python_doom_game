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
        self.npc_positions: set[Tuple[int, int]] = {}

        # sprites
        add_sprite(AnimatedSprite(game))
        add_sprite(SpriteObject(game))

        # npc
        add_npc(NPC(game))
        add_npc(NPC(game, position=(12.5, 7.5)))
        add_npc(NPC(game, position=(13.5, 4.5)))

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def update(self):
        self.npc_positions = {npc.map_position for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
