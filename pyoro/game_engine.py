import sys
import typing

from pyoro.banks.image_bank import ImageBank
from pyoro.configuration import Configuration
from pyoro.entities.entity_orchestrator import EntityOrchestrator
from pyoro.events.event import Event
from pyoro.events.event_dispatcher import EventDispatcher
from pyoro.events.event_kind import EventKind
from pyoro.events.event_listener import EventListener
from pyoro.exceptions.already_initialized import AlreadyInitializedException
from pyoro.game_state import GameMode, GameState
from pyoro.graphics.graphics_manager import GraphicsManager


class GameEngine:
    _instance: typing.ClassVar[typing.Self | None] = None

    def __init__(self):
        if self._instance is not None:
            raise AlreadyInitializedException(
                f"'{self.__class__.__name__}' already initialized"
            )

        GraphicsManager()  # force GraphicsManager initialization

        self.game_state: GameState | None = None
        self.entity_orchestrator: EntityOrchestrator | None = None

        event_dispatcher = EventDispatcher.get_instance()
        event_dispatcher.add_listener(EventListener(EventKind.TICK, self.on_event))
        event_dispatcher.add_listener(
            EventListener(EventKind.ASSETS_LOADED, self.on_event)
        )
        event_dispatcher.add_listener(
            EventListener(EventKind.GUI_BUTTON_CLICK, self.on_event)
        )

    @classmethod
    def get_instance(cls) -> typing.Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start_splash(self):
        graphics_manager = GraphicsManager.get_instance()
        graphics_manager.set_splash_view()

        configuration = Configuration.get_instance()
        configuration.load()

        image_bank = ImageBank.get_instance()
        image_bank.load()

    def quit(self):
        sys.exit(0)

    def start_main_menu(self):
        self.game_state = GameState(mode=GameMode.TONGUE)
        self.entity_orchestrator = EntityOrchestrator(self.game_state)

        graphics_manager = GraphicsManager.get_instance()
        graphics_manager.set_main_menu_view()

    def start_game(self, mode: GameMode):
        self.game_state = GameState(mode)
        self.entity_orchestrator = EntityOrchestrator(self.game_state)

        graphics_manager = GraphicsManager.get_instance()
        graphics_manager.set_game_view()

    def start_settings_menu(self):
        graphics_manager = GraphicsManager.get_instance()
        graphics_manager.set_settings_menu_view()

    def on_tick(self, deltatime: float):
        graphics_manager = GraphicsManager.get_instance()
        graphics_manager.update(deltatime)

    def on_event(self, event: Event):
        match event.get_kind():
            case EventKind.TICK:
                return self.on_tick(event.get_metadata().get("deltatime", 0.0))
            case EventKind.ASSETS_LOADED:
                return self.start_main_menu()
            case EventKind.GUI_BUTTON_CLICK:
                match event.get_metadata().get("button_id", None):
                    case "main_menu_play_tongue":
                        return self.start_game(GameMode.TONGUE)
                    case "main_menu_play_seed":
                        return self.start_game(GameMode.SHOOT)
                    case "main_menu_quit":
                        return self.quit()
                    case _:
                        return None
            case _:
                return None
