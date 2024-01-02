from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from main import Game

GameType = TypeVar("GameType", bound="Game")
