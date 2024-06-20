from pyoro.events.event_dispatcher import EventDispatcher
from pyoro.events.event import Event
from pyoro.events.event_kind import EventKind
from pyoro.graphics.layers.gui_layers.gui_layer import GuiLayer
from pyoro.graphics.widgets.image import Image
from pyoro.graphics.widgets.image_button import ImageButton
from pyoro.graphics.widgets.anchor import AnchorX, AnchorY
from pyoro.graphics.widgets.text_button import TextButton
from pyoro.graphics.window import Window


class MainMenuGuiLayer(GuiLayer):
    def __init__(self):
        super().__init__()

        window = Window.get_instance()

        self.title = Image(
            self.batch,
            self.group,
            window.width // 2,
            window.height // 4,
            "gui_title",
            anchor_x=AnchorX.CENTER,
            anchor_y=AnchorY.CENTER,
        )
        self.play_tongue_button = ImageButton(  # type: ignore
            self.batch,
            self.group,
            window.width // 4,
            window.height // 2,
            self.on_play_tongue,
            "gui_button_play_tongue",
            "gui_button_play_tongue_pressed",
            "gui_button_play_tongue_hover",
            anchor_x=AnchorX.CENTER,
            anchor_y=AnchorY.CENTER,
        )
        self.play_seed_button = ImageButton(
            self.batch,
            self.group,
            window.width // 4 * 3,
            window.height // 2,
            self.on_play_seed,
            "gui_button_play_seed",
            "gui_button_play_seed_pressed",
            "gui_button_play_seed_hover",
            anchor_x=AnchorX.CENTER,
            anchor_y=AnchorY.CENTER,
        )
        self.settings_button = TextButton(
            self.batch,
            self.group,
            window.width // 2,
            window.height // 4 * 3,
            self.on_settings,
            "Settings",
            anchor_x=AnchorX.CENTER,
            anchor_y=AnchorY.CENTER,
        )
        self.quit_button = TextButton(
            self.batch,
            self.group,
            window.width // 2,
            window.height // 4,
            self.on_quit,
            "Quit",
            anchor_x=AnchorX.CENTER,
            anchor_y=AnchorY.CENTER,
        )

    def on_play_tongue(self):
        event_dispatcher = EventDispatcher.get_instance()
        event_dispatcher.push(
            Event(EventKind.GUI_BUTTON_CLICK, {"button_id": "main_menu_play_tongue"})
        )

    def on_play_seed(self):
        event_dispatcher = EventDispatcher.get_instance()
        event_dispatcher.push(
            Event(EventKind.GUI_BUTTON_CLICK, {"button_id": "main_menu_play_seed"})
        )

    def on_settings(self):
        event_dispatcher = EventDispatcher.get_instance()
        event_dispatcher.push(
            Event(EventKind.GUI_BUTTON_CLICK, {"button_id": "main_menu_settings"})
        )

    def on_quit(self):
        event_dispatcher = EventDispatcher.get_instance()
        event_dispatcher.push(
            Event(EventKind.GUI_BUTTON_CLICK, {"button_id": "main_menu_quit"})
        )
