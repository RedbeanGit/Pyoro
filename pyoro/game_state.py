import enum


class GameMode(enum.Enum):
    TONGUE = 0
    SHOOT = 1


class GameState:
    __slots__ = ("mode", "size", "speed")

    def __init__(self, mode: GameMode):
        self.mode = mode
        self.size = (32, 18)
        self.speed = 1.0
