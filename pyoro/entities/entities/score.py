import pyglet
import typing

from entities.entity import Entity
from animation import Animation
from pyoro.game_state import GameState


class Score(Entity):
    IMAGE_IDS = (
        "score_10",
        "score_50",
        "score_100",
        "score_300_0",
        "score_300_1",
        "score_300_2",
        "score_300_3",
        "score_300_4",
        "score_300_5",
        "score_1000_0",
        "score_1000_1",
        "score_1000_2",
        "score_1000_3",
        "score_1000_4",
        "score_1000_5",
    )
    BLINK_INTERVAL = 0.05
    LIFE_TIME = 1
    SIZE = (1.5, 0.7)
    HITBOX_SIZE = (0, 0, 0, 0)

    def __init__(self, pos: tuple[float, float], value: int):
        super().__init__(pos)
        self.value = value

        if value in (10, 50, 100):
            self.image_id = f"score_{value}"
        elif value in (300, 1000):
            self.animation = Animation(
                [f"score_{value}_{i}" for i in range(6)], self.BLINK_INTERVAL
            )

        pyglet.clock.schedule_once(self.remove, self.LIFE_TIME)  # type: ignore

    def update(
        self, delta: float, others: typing.Iterable[Entity], game_state: GameState
    ):
        if self.value in (300, 1000):
            pass
            # self.image_id = self.animation.get()
        return super().update(delta, others, game_state)

    def remove(self, _dt: float):
        self.dead = True
