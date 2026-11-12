from typing import Protocol, TypeVar, runtime_checkable


PlayerType = TypeVar("PlayerType")
MoveType = TypeVar("MoveType")


@runtime_checkable
class GameInterface(Protocol[PlayerType, MoveType]):
    @property
    def players(self) -> list[PlayerType]:
        ...

    def make_move(self, player: PlayerType) -> MoveType:
        ...
