import typing

from pyoro.entities.entities.entity import Entity
from pyoro.game_state import GameState


class Case(Entity):
    IMAGE_IDS = ("case",)
    FALL_SPEED = 25

    def __init__(self, pos: tuple[float, float], is_ready: bool = True):
        super().__init__(pos)
        self.image_id = "case"
        self.is_destroying = False
        self.is_ready = is_ready

        if not is_ready:
            self.vel = (0, -Angel.SPEED)

    def update(
        self, delta: float, others: typing.Iterable[Entity], game_state: GameState
    ):
        super().update(delta, others, game_state)

        if not self.is_ready:
            if self.pos[1] <= self.SIZE[1] / 2:
                self.is_ready = True
                self.vel = (0, 0)
                self.pos = (self.pos[0], self.SIZE[1] / 2)
            else:
                self.vel = (0, -Angel.SPEED)

    def destroy(self):
        self.is_destroying = True
        self.vel = (0, -self.FALL_SPEED)

    def on_outside(self):
        self.dead = True
        return super().on_outside()
