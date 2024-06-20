import pyglet
import random
import typing

from pyoro.entities.entities.abstract_bean import BeanType
from pyoro.entities.entities.angel import Angel
from pyoro.entities.entities.bean_green import BeanGreen
from pyoro.entities.entities.bean_pink import BeanPink
from pyoro.entities.entities.case import Case
from pyoro.entities.entities.entity import Direction, Entity
from pyoro.entities.entities.pyoro import Pyoro
from pyoro.entities.entities.pyoro2 import Pyoro2
from pyoro.entities.entities.score import Score
from pyoro.entities.entities.tongue import Tongue
from pyoro.game_state import GameMode, GameState


class EntityOrchestrator:
    def __init__(self, game_state: GameState):
        super().__init__()
        self.game_state = game_state
        self.entities: list[Entity] = []

    def has_tongue(self) -> bool:
        return any(isinstance(entity, Tongue) for entity in self.entities)

    def get_pyoro(self) -> Pyoro | Pyoro2 | None:
        return next(
            (
                entity
                for entity in self.entities
                if isinstance(entity, Pyoro) or isinstance(entity, Pyoro2)
            ),
            None,
        )

    def get_cases(self) -> list[Case]:
        return [entity for entity in self.entities if isinstance(entity, Case)]

    def spawn_pyoro(self):
        match self.game_state.mode:
            case GameMode.TONGUE:
                self.entities.append(
                    Pyoro((1 + Pyoro.SIZE[0] / 2, 1 + Pyoro.SIZE[1] / 2))
                )
            case GameMode.SHOOT:
                self.entities.append(
                    Pyoro2((1 + Pyoro2.SIZE[0] / 2, 1 + Pyoro2.SIZE[1] / 2))
                )

    def spawn_cases(self):
        nb_cases = self.game_state.size[0] // Case.SIZE[0]

        for i in range(nb_cases):
            case = Case((i + Case.SIZE[0] / 2, Case.SIZE[1] / 2))
            self.entities.append(case)

    def spawn_bean(self, bean_type: BeanType = BeanType.GREEN):
        pos_x = random.randint(0, self.game_state.size[0])
        pos_y = self.game_state.size[1]
        bean: BeanGreen | BeanPink | None = None

        if bean_type == BeanType.GREEN:
            bean = BeanGreen(
                (pos_x + BeanGreen.SIZE[0] / 2, pos_y - BeanGreen.SIZE[1] / 2)
            )
        elif bean_type == BeanType.PURPLE:
            bean = BeanPink(
                (pos_x + BeanPink.SIZE[0] / 2, pos_y - BeanPink.SIZE[1] / 2),
                self.spawn_angel,
            )

        if bean:
            self.entities.append(bean)

    def spawn_tongue(self):
        def add_score(get_score: typing.Callable[[GameState], int]):
            # score = get_score(self.game_state)
            pass

        pyoro = self.get_pyoro()
        if pyoro and not self.has_tongue():
            if pyoro.direction == Direction.LEFT:
                pos_x = pyoro.pos[0] - Tongue.SIZE[0] / 2 - Tongue.POS_OFFSET[0]
            else:
                pos_x = pyoro.pos[0] + Tongue.SIZE[0] / 2 + Tongue.POS_OFFSET[0]
            pos_y = pyoro.pos[1] + Tongue.SIZE[1] / 2 + Tongue.POS_OFFSET[1]
            self.tongue = Tongue((pos_x, pos_y), pyoro.direction, add_score)

    def spawn_score(self, pos: tuple[float, float], value: int):
        score = Score((pos[0] - Score.SIZE[0] / 2, pos[1] - Score.SIZE[1] / 2), value)
        self.entities.append(score)

    def spawn_angel(self):
        def find_missing_case():
            nb_cases = self.game_state.size[0] // Case.SIZE[0]
            all_positions = list(range(nb_cases))
            for case in self.get_cases():
                case_pose_x = case.pos[0] - case.SIZE[0] / 2
                if not case.dead and case_pose_x in all_positions:
                    all_positions.remove(case_pose_x)
            return all_positions

        missing_cases = find_missing_case()
        if missing_cases:
            pos_x = missing_cases[0] + Case.SIZE[1] / 2
            pos_y = self.game_state.size[1]

            angel = Angel((pos_x, pos_y + Angel.SIZE[1] / 2))
            self.entities.append(angel)

            new_case = Case((pos_x, pos_y - Angel.ARMS_LENGTH), is_ready=False)
            self.entities.append(new_case)

    def schedule_bean_spawn(self):
        def on_spawn_bean(_delta: float):
            bean_type_repartition = (
                [BeanType.GREEN] * 10 + [BeanType.PURPLE] * 3 + [BeanType.SILVER] * 1
            )
            self.spawn_bean(random.choice(bean_type_repartition))
            pyglet.clock.schedule_once(  # type: ignore
                on_spawn_bean,
                BeanGreen.SPAWN_INTERVAL
                / self.game_state.speed**2
                / (random.random() + 1),
            )

        pyglet.clock.schedule_once(on_spawn_bean, BeanGreen.SPAWN_INTERVAL)  # type: ignore

    def update(self, delta: float):
        for entity in self.entities:
            entity.update(
                delta * self.game_state.speed, list(self.entities), self.game_state
            )

        if self.tongue and self.tongue.dead:
            self.tongue = None
