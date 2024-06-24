import enum
import pyglet
import typing

from pyoro.entities.entities.abstract_pyoro import AbstractPyoro
from pyoro.entities.entities.case import Case
from pyoro.entities.entities.entity import Entity
from pyoro.game_state import GameState


class BeanType(enum.Enum):
    GREEN = 0
    PURPLE = 1
    SILVER = 2


class AbstractBean(Entity):
    FALL_SPEED = 0.1
    SPRITE_UPDATE_INTERVAL = 0.1
    EXPLOSION_SPRITE_UPDATE_INTERVAL = 0.1

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos)
        self.vel = (0, -self.FALL_SPEED)
        self.animation = None
        self.is_exploding = False

    def update(
        self, delta: float, others: typing.Iterable[Entity], game_state: GameState
    ):
        super().update(delta, others, game_state)

    def on_outside(self):
        self.dead = True
        return super().on_outside()

    def on_collision(self, other: Entity):
        if not self.is_exploding:
            if isinstance(other, AbstractPyoro):
                self.explode()
                other.die()
            elif isinstance(other, Case) and other.is_ready and not other.is_destroying:
                self.explode()
                other.destroy()

    def explode(self):
        def die(_):
            self.dead = True

        self.is_exploding = True
        self.vel = (0, 0)
        pyglet.clock.schedule_once(die, 0.5)  # type: ignore

    def catch(self):
        self.dead = True
