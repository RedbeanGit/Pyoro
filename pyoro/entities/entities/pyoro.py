from pyoro.entities.entities.abstract_pyoro import AbstractPyoro


class Pyoro(AbstractPyoro):
    IMAGE_IDS = (
        "pyoro_normal",
        "pyoro_dead",
        "pyoro_tongue",
        "pyoro_eat",
        "pyoro_jump",
    )

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos)
        self.image_id = "pyoro_normal"
        self.eating = False

    def start_move(self, direction: Direction):
        if not self.eating:
            return super().start_move(direction)
        return None

    def start_eating(self):
        if not self.dead:
            self.eating = True
            self.vel = (0, 0)
            self.image_id = "pyoro_tongue"

    def stop_eating(self):
        self.eating = False
        self.image_id = "pyoro_normal"

    def die(self):
        self.stop_eating()
        self.image_id = "pyoro_dead"
        return super().die()
