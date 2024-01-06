from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from main import Game
    from sprite_object import *

GameType = TypeVar("GameType", bound="Game")
AnimatedSpriteType = TypeVar("AnimatedSpriteType", bound="AnimatedSprite")
SpriteObjectType = TypeVar("SpriteObjectType", bound="SpriteObject")
