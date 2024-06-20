import enum
import typing

from pyoro.game_state import GameState


class Direction(enum.Enum):
    LEFT = -1
    RIGHT = 1


# We need to define these types before the Entity class to prevent undefined references.
type Entities = typing.Iterable[Entity]
type EntityType = Entity


class Entity:
    SIZE = (1, 1)
    HITBOX = (-0.5, -0.5, 1, 1)
    IMAGE_IDS = []

    def __init__(self, pos: tuple[float, float]):
        self.pos: tuple[float, float] = pos
        self.vel: tuple[float, float] = (0, 0)
        self.direction: Direction = Direction.RIGHT

    def update(self, delta: float, others: Entities, game_state: GameState):
        self.pos = (
            self.pos[0] + self.vel[0] * delta,
            self.pos[1] + self.vel[1] * delta,
        )

        def collides(other: Entity):
            hitbox_pos = (
                self.pos[0] + self.HITBOX[0],
                self.pos[1] + self.HITBOX[1],
                self.pos[0] + self.HITBOX[0] + self.HITBOX[2],
                self.pos[1] + self.HITBOX[1] + self.HITBOX[3],
            )
            other_hitbox_pos = (
                other.pos[0] + other.HITBOX[0],
                other.pos[1] + other.HITBOX[1],
                other.pos[0] + other.HITBOX[0] + other.HITBOX[2],
                other.pos[1] + other.HITBOX[1] + other.HITBOX[3],
            )
            return (
                hitbox_pos[0] < other_hitbox_pos[2]
                and hitbox_pos[2] > other_hitbox_pos[0]
                and hitbox_pos[1] < other_hitbox_pos[3]
                and hitbox_pos[3] > other_hitbox_pos[1]
            )

        def outside():
            return (
                self.pos[0] + self.SIZE[0] / 2 < 0
                or self.pos[0] - self.SIZE[0] / 2 > game_state.size[0]
                or self.pos[1] + self.SIZE[1] / 2 < 0
                or self.pos[1] - self.SIZE[1] / 2 > game_state.size[1]
            )

        for entity in others:
            if entity is self:
                continue
            if collides(entity):
                self.on_collision(entity)
            if outside():
                self.on_outside()

    def on_collision(self, other: EntityType):
        """This method is called when the entity collides with another entity."""
        pass

    def on_outside(self):
        """This method is called when the entity is outside the game area."""
        pass
