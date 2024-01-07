from typing import Deque, Literal, TypeVar, TYPE_CHECKING

from pygame import Surface

if TYPE_CHECKING:
    from main import Game

GameType = TypeVar("GameType", bound="Game")

MiniMapType = list[
    bool | int
]

WorldMapType = dict[tuple[int, int], int]

ImagesType = Deque[Surface]

RayCastResultType = list[
    tuple[float, float, int, float]
]

ObjectsToRenderType = list[
    tuple[
        float,
        Surface,
        tuple[int, float] | tuple[int, Literal[0]]
    ]
]
