import math
import typing

from entities.abstract_bean import AbstractBean
from entities.entity import Direction, Entity
from entities.pyoro import Pyoro
from pyoro.game_state import GameState


class Tongue(Entity):
    SIZE = (1.2, 1.2)
    HITBOX = (-0.8, -0.8, 1.6, 1.6)
    IMAGE_IDS = ("tongue",)
    SPEED = 40
    ANGLE = math.pi / 4
    POS_OFFSET = (0, -0.25)

    def __init__(
        self,
        pos: tuple[float, float],
        direction: Direction,
        on_catch: typing.Callable[[typing.Callable[[GameState], int]], None],
    ):
        super().__init__(pos)

        self.image_id = "tongue"
        self.direction = direction
        self.handle_catch = on_catch
        self.extending = False

    def extend(self):
        self.extending = True
        self.vel = (
            self.SPEED * math.cos(self.ANGLE) * self.direction.value,
            self.SPEED * math.sin(self.ANGLE),
        )

    def retract(self):
        self.extending = False
        self.vel = (
            -1.8 * self.SPEED * math.cos(self.ANGLE) * self.direction.value,
            -1.8 * self.SPEED * math.sin(self.ANGLE),
        )

    def on_collision(self, other: Entity):
        if isinstance(other, AbstractBean) and self.extending:
            self.retract()
            self.handle_catch(self.calculate_score)
            other.catch()

        if isinstance(other, Pyoro) and not self.extending:
            other.stop_eating()
            self.dead = True

    def on_outside(self):
        if self.pos[1] > 0:
            self.retract()
        else:
            self.dead = True

    def calculate_score(self, game_state: GameState) -> int:
        ratio = self.pos[1] / game_state.size[1]

        if ratio >= 0.8:
            return 1000
        if ratio >= 0.6:
            return 300
        if ratio >= 0.4:
            return 100
        if ratio >= 0.2:
            return 50
        return 10
