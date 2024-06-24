import typing

from pyoro.entities.entities.entity import Entity
from pyoro.game_state import GameState


class Angel(Entity):
    SPEED = 10
    ARMS_LENGTH = 1.5

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos)
        self.vel = (0, -self.SPEED)

    def update(
        self, delta: float, others: typing.Iterable[Entity], game_state: GameState
    ):
        super().update(delta, others, game_state)

        if self.pos[1] <= self.ARMS_LENGTH + 0.5:
            self.vel = (0, self.SPEED)

    def on_outside(self):
        self.dead = True
        return super().on_outside()
