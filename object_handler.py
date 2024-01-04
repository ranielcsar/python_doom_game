from sprite_object import *


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.static_sprite_path = "resources/sprites/static_sprites/"
        self.animated_sprite_path = "resources/sprites/animated_sprites/"
        add_sprite = self.add_sprite

        add_sprite(AnimatedSprite(game))
        add_sprite(SpriteObject(game))

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def update(self):
        [sprite.update() for sprite in self.sprite_list]
