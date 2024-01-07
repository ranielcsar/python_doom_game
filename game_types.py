from typing import Deque, Dict, Literal, Tuple, TypeVar, TYPE_CHECKING, Union

from pygame import Surface

if TYPE_CHECKING:
    from main import Game

GameType = TypeVar("GameType", bound="Game")
MiniMapType = list[Union[bool, int]]
WorldMapType = Dict[Tuple[int, int], int]
ImagesType = Deque[Surface]
RayCastResultType = list[Tuple[float, float, int, float]]
ObjectsToRenderType = list[
    Tuple[float, Surface, tuple[int, float] | tuple[int, Literal[0]]]
]
