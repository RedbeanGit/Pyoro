import typing

from math import ceil

from pyoro.entities.entities.entity import Direction, Entity
from pyoro.game_state import GameState


class AbstractPyoro(Entity):
    SPEED = 0.1

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos)
        self.vel = (0, 0)
        self.direction = Direction.LEFT
        self.is_dying = False

    def start_move(self, direction: Direction):
        if not self.is_dying:
            self.direction = direction
            self.vel = (direction.value * self.SPEED, 0)

    def stop_move(self):
        self.vel = (0, 0)

    def update(
        self, delta: float, others: typing.Iterable[Entity], game_state: GameState
    ):
        super().update(delta, others, game_state)

        def has_front_case():
            if self.direction == Direction.LEFT:
                front_case_pos_x = (
                    ceil(self.pos[0] - self.SIZE[0] / 2) - Case.SIZE[0] / 2
                )
            else:
                front_case_pos_x = (
                    int(self.pos[0] + AbstractPyoroConfig.SIZE[0] / 2)
                    + Case.SIZE[0] / 2
                )

            for entity in others:
                if (
                    isinstance(entity, Case)
                    and entity.pos[0] == front_case_pos_x
                    and entity.is_ready
                    and not entity.is_destroying
                ):
                    return entity
            return False

        if self.is_dying:
            return None
        if self.pos[0] - AbstractPyoroConfig.SIZE[0] / 2 < 0:
            self.pos = (AbstractPyoroConfig.SIZE[0] / 2, self.pos[1])
            self.stop_move()
        elif self.pos[0] + AbstractPyoroConfig.SIZE[0] / 2 > game_state.size[0]:
            self.pos = (
                game_state.size[0] - AbstractPyoroConfig.SIZE[0] / 2,
                self.pos[1],
            )
            self.stop_move()

        if not has_front_case():
            if self.direction == Direction.LEFT:
                self.pos = (
                    ceil(self.pos[0] - AbstractPyoroConfig.SIZE[0] / 2)
                    + AbstractPyoroConfig.SIZE[0] / 2,
                    self.pos[1],
                )
            else:
                self.pos = (
                    int(self.pos[0] + AbstractPyoroConfig.SIZE[0] / 2)
                    - AbstractPyoroConfig.SIZE[0] / 2,
                    self.pos[1],
                )

    def die(self):
        self.is_dying = True
        self.stop_move()
        self.vel = (0, -10)

    def on_outside(self):
        if self.is_dying:
            self.dead = True
        return super().on_outside()
