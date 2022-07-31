# -*- coding: utf-8 -*-

# 	This file is part of Pyoro (A Python fan game).
#
# 	Metawars is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	Metawars is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
Provide a menu to manage game options.

Created on 21/08/2018
"""

import os
from pygame.locals import KEYDOWN, JOYBUTTONDOWN, JOYAXISMOTION, JOYHATMOTION

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH, NAME, VERSION
from game.util import get_key_name, get_joy_key_name, reset_game, Game

from gui.button import Button
from gui.setting_bar import SettingBar
from gui.text import Text
from gui.menu_widget import MenuWidget


class OptionMenu(MenuWidget):
    """
    Create a menu allowing the player to change some game settings.
    """

    DEFAULT_KWARGS = {"font": os.path.join(GUI_IMAGE_PATH, "font.ttf"), "font_size": 20}

    def __init__(self, activity, pos, quit_fct, **kwargs):
        """
        Initialize a new Option_menu widget.

        :type activity: gui.activity.Activity
        :param activity: The parent activity of this widget.

        :type pos: tuple
        :param pos: The default position of this widget in a (x, y) tuple where
            x and y are integers.

        :type quit_fct: callable
        :param quit_fct: A function, method or class which can be called when the
            player leave this menu.
        """

        OptionMenu.update_default_kwargs(kwargs)
        MenuWidget.__init__(self, activity, pos, **kwargs)

        self.quit_fct = quit_fct
        self.waiting_input = ()

    def init_widgets(self):
        """
        Create sub_widgets which will be display in this menu.
        """

        font = self.kwargs["font"]
        width, height = self.kwargs["size"]
        keyboard_options = Game.options.get("keyboard", {})
        joystick_options = Game.options.get("joystick", {})
        music_volume = Game.options.get("music volume", 1)
        sound_volume = Game.options.get("sound volume", 1)
        font_size = self.kwargs["font_size"]
        medium_font_size = font_size - 3
        mini_font_size = medium_font_size - 3

        pos_x = int(width * 0.05)
        pos_y = int(height * 0.15)
        self.add_sub_widget(
            "volumeMusicText",
            Text,
            (pos_x, pos_y),
            "Volume de la musique",
            anchor=(-1, 0),
            font_size=medium_font_size,
            font=font,
        )

        pos_y = int(height * 0.25)
        self.add_sub_widget(
            "volumeSoundText",
            Text,
            (pos_x, pos_y),
            "Volume des sons",
            anchor=(-1, 0),
            font_size=medium_font_size,
            font=font,
        )

        pos_y = int(height * 0.35)
        self.add_sub_widget(
            "commandTitleText",
            Text,
            (pos_x, pos_y),
            "Commandes :",
            anchor=(-1, 0),
            font_size=medium_font_size,
            font=font,
        )

        pos_x = int(width * 0.15)
        pos_y = int(height * 0.45)
        self.add_sub_widget(
            "rightCommandText",
            Text,
            (pos_x, pos_y),
            "Aller a droite",
            anchor=(-1, 0),
            font_size=medium_font_size,
            font=font,
        )

        pos_y = int(height * 0.55)
        self.add_sub_widget(
            "leftCommandText",
            Text,
            (pos_x, pos_y),
            "Aller a gauche",
            anchor=(-1, 0),
            font_size=medium_font_size,
            font=font,
        )

        pos_y = int(height * 0.65)
        self.add_sub_widget(
            "actionCommandText",
            Text,
            (pos_x, pos_y),
            "Tirer (la langue)",
            anchor=(-1, 0),
            font_size=medium_font_size,
            font=font,
        )

        pos_y = int(height * 0.75)
        self.add_sub_widget(
            "pauseCommandText",
            Text,
            (pos_x, pos_y),
            "Pause / retour",
            anchor=(-1, 0),
            font_size=medium_font_size,
            font=font,
        )

        pos_x = int(width * 0.25)
        pos_y = int(height * 0.95)
        self.add_sub_widget(
            "resetButton",
            Button,
            (pos_x, pos_y),
            text="Réinitialiser",
            anchor=(0, 0),
            text_kwargs={"font_size": medium_font_size, "font": font},
            size=(int(width * 0.4), int(height * 0.06)),
            on_click_fct=reset_game,
        )

        pos_x = int(width * 0.5)
        pos_y = int(height * 0.05)
        self.add_sub_widget(
            "titleText",
            Text,
            (pos_x, pos_y),
            "Options",
            anchor=(0, -1),
            font_size=font_size,
            font=font,
        )

        pos_x = int(width * 0.66)
        pos_y = int(height * 0.35)
        self.add_sub_widget(
            "keyboardCommandText",
            Text,
            (pos_x, pos_y),
            "Clavier",
            anchor=(0, 0),
            font_size=medium_font_size,
            font=font,
        )

        pos_y = int(height * 0.45)
        self.add_sub_widget(
            ("commandButton", "keyboard", "right"),
            Button,
            (pos_x, pos_y),
            text=get_key_name(keyboard_options["right"]),
            size=(int(width * 0.18), int(height * 0.08)),
            on_click_fct=self.input_command,
            on_click_args=("keyboard", "right"),
            anchor=(0, 0),
            text_kwargs={"font_size": mini_font_size, "font": font},
        )

        pos_y = int(height * 0.55)
        self.add_sub_widget(
            ("commandButton", "keyboard", "left"),
            Button,
            (pos_x, pos_y),
            text=get_key_name(keyboard_options["left"]),
            size=(int(width * 0.18), int(height * 0.08)),
            on_click_fct=self.input_command,
            on_click_args=("keyboard", "left"),
            anchor=(0, 0),
            text_kwargs={"font_size": mini_font_size, "font": font},
        )

        pos_y = int(height * 0.65)
        self.add_sub_widget(
            ("commandButton", "keyboard", "action"),
            Button,
            (pos_x, pos_y),
            text=get_key_name(keyboard_options["action"]),
            size=(int(width * 0.18), int(height * 0.08)),
            on_click_fct=self.input_command,
            on_click_args=("keyboard", "action"),
            anchor=(0, 0),
            text_kwargs={"font_size": mini_font_size, "font": font},
        )

        pos_y = int(height * 0.75)
        self.add_sub_widget(
            ("commandButton", "keyboard", "pause"),
            Button,
            (pos_x, pos_y),
            text=get_key_name(keyboard_options["pause"]),
            size=(int(width * 0.18), int(height * 0.08)),
            on_click_fct=self.input_command,
            on_click_args=("keyboard", "pause"),
            anchor=(0, 0),
            text_kwargs={"font_size": mini_font_size, "font": font},
        )

        pos_x = int(width * 0.75)
        pos_y = int(height * 0.95)
        self.add_sub_widget(
            "backButton",
            Button,
            (pos_x, pos_y),
            text="Retour",
            anchor=(0, 0),
            text_kwargs={"font_size": medium_font_size, "font": font},
            size=(int(width * 0.4), int(height * 0.06)),
            on_click_fct=self.destroy,
        )

        pos_x = int(width * 0.86)
        pos_y = int(height * 0.35)
        self.add_sub_widget(
            "joystickCommandText",
            Text,
            (pos_x, pos_y),
            "Manette",
            anchor=(0, 0),
            font_size=medium_font_size,
            font=font,
        )

        pos_y = int(height * 0.45)
        self.add_sub_widget(
            ("commandButton", "joystick", "right"),
            Button,
            (pos_x, pos_y),
            text=get_joy_key_name(**joystick_options["right"]),
            size=(int(width * 0.18), int(height * 0.08)),
            on_click_fct=self.input_command,
            on_click_args=("joystick", "right"),
            anchor=(0, 0),
            text_kwargs={"font_size": mini_font_size, "font": font},
        )

        pos_y = int(height * 0.55)
        self.add_sub_widget(
            ("commandButton", "joystick", "left"),
            Button,
            (pos_x, pos_y),
            text=get_joy_key_name(**joystick_options["left"]),
            size=(int(width * 0.18), int(height * 0.08)),
            on_click_fct=self.input_command,
            on_click_args=("joystick", "left"),
            anchor=(0, 0),
            text_kwargs={"font_size": mini_font_size, "font": font},
        )

        pos_y = int(height * 0.65)
        self.add_sub_widget(
            ("commandButton", "joystick", "action"),
            Button,
            (pos_x, pos_y),
            text=get_joy_key_name(**joystick_options["action"]),
            size=(int(width * 0.18), int(height * 0.08)),
            on_click_fct=self.input_command,
            on_click_args=("joystick", "action"),
            anchor=(0, 0),
            text_kwargs={"font_size": mini_font_size, "font": font},
        )

        pos_y = int(height * 0.75)
        self.add_sub_widget(
            ("commandButton", "joystick", "pause"),
            Button,
            (pos_x, pos_y),
            text=get_joy_key_name(**joystick_options["pause"]),
            size=(int(width * 0.18), int(height * 0.08)),
            on_click_fct=self.input_command,
            on_click_args=("joystick", "pause"),
            anchor=(0, 0),
            text_kwargs={"font_size": mini_font_size, "font": font},
        )

        pos_x = int(width * 0.95)
        pos_y = int(height * 0.15)
        self.add_sub_widget(
            ("volumeSettingBar", "music"),
            SettingBar,
            (pos_x, pos_y),
            anchor=(1, 0),
            size=(int(width * 0.45), int(height * 0.05)),
            cursor_width=int(width * 0.03),
            line_thickness=int(height * 0.02),
            value=music_volume,
        )

        pos_y = int(height * 0.25)
        self.add_sub_widget(
            ("volumeSettingBar", "sound"),
            SettingBar,
            (pos_x, pos_y),
            anchor=(1, 0),
            size=(int(width * 0.45), int(height * 0.05)),
            cursor_width=int(width * 0.03),
            line_thickness=int(height * 0.02),
            value=sound_volume,
        )

        pos_y = int(height * 0.85)
        self.add_sub_widget(
            "versionText",
            Text,
            (pos_x, pos_y),
            f"{NAME} v{VERSION}",
            font=font,
            font_size=mini_font_size,
            anchor=(1, 0),
        )

    def on_event(self, event):
        """
        Update sub_widgets of this menu by passing to the given event.

        :type event: pygame.event.Event
        :param event: The pygame event to give to all sub_widgets.
        """

        MenuWidget.on_event(self, event)
        if self.waiting_input:
            if self.waiting_input[0] == "keyboard":
                if event.type == KEYDOWN:
                    self.config_sub_widget(
                        ("commandButton", *self.waiting_input),
                        text=get_key_name(event.key),
                        enable=True,
                    )
                    self.set_keyboard_option(self.waiting_input[1], event.key)
                    self.waiting_input = ()

            elif self.waiting_input[0] == "joystick":

                if event.type == JOYBUTTONDOWN:
                    self.config_sub_widget(
                        ("commandButton", *self.waiting_input),
                        text=get_joy_key_name(JOYBUTTONDOWN, buttonId=event.button),
                        enable=True,
                    )
                    self.set_joystick_option(
                        self.waiting_input[1],
                        inputType=JOYBUTTONDOWN,
                        buttonId=event.button,
                    )
                    self.waiting_input = ()

                elif event.type == JOYHATMOTION:
                    self.config_sub_widget(
                        ("commandButton", *self.waiting_input),
                        text=get_joy_key_name(
                            JOYHATMOTION, hatId=event.hat, value=round(event.value)
                        ),
                        enable=True,
                    )
                    self.set_joystick_option(
                        self.waiting_input[1],
                        inputType=JOYHATMOTION,
                        hatId=event.hat,
                        value=round(event.value),
                    )
                    self.waiting_input = ()

                elif event.type == JOYAXISMOTION:
                    self.config_sub_widget(
                        ("commandButton", *self.waiting_input),
                        text=get_joy_key_name(
                            JOYAXISMOTION, axisId=event.axis, value=round(event.value)
                        ),
                        enable=True,
                    )
                    self.set_joystick_option(
                        self.waiting_input[1],
                        inputType=JOYAXISMOTION,
                        axisId=event.axis,
                        value=round(event.value),
                    )
                    self.waiting_input = ()

                elif event.type == KEYDOWN:
                    self.config_sub_widget(
                        ("commandButton", *self.waiting_input), enable=True
                    )
                    self.waiting_input = ()

    def set_keyboard_option(self, action_name, key_code):
        """
        Define a new key for a given action.

        :type action_name: str
        :param action_name: The name used to identify the associated action.

        :type key_code: int
        :param key_code: A key id.
        """

        if "keyboard" not in Game.options:
            Game.options["keyboard"] = {}
        Game.options["keyboard"][action_name] = key_code

    def set_joystick_option(self, action_name, **inputKwargs):
        """
        Define a new controller button for a given action.

        :type action_name: str
        :param action_name: The name used to identify the associated action.

        Keyword arguments depend of the event type.
        """

        if "joystick" not in Game.options:
            Game.options["joystick"] = {}
        Game.options["joystick"][action_name] = inputKwargs

    def update(self, delta_time):
        """
        Update the menu, its sub_widgets and the sound volume.

        :type delta_time: float
        :param delta_time: Time elapsed since the last call of this method (in
            seconds).
        """

        MenuWidget.update(self, delta_time)

        if ("volumeSettingBar", "music") in self.sub_widgets:
            Game.audio_player.music_volume = self.sub_widgets[
                "volumeSettingBar", "music"
            ].get_value()
        if ("volumeSettingBar", "sound") in self.sub_widgets:
            Game.audio_player.sound_volume = self.sub_widgets[
                "volumeSettingBar", "sound"
            ].get_value()

    def destroy(self):
        """
        Destroy the menu and its sub_widgets.
        """

        if ("volumeSettingBar", "music") in self.sub_widgets:
            Game.options["music volume"] = self.sub_widgets[
                "volumeSettingBar", "music"
            ].get_value()
        if ("volumeSettingBar", "sound") in self.sub_widgets:
            Game.options["sound volume"] = self.sub_widgets[
                "volumeSettingBar", "sound"
            ].get_value()
        MenuWidget.destroy(self)
        self.quit_fct()

    def input_command(self, input_type_name, action_name):
        """
        Start to record user event to configure the keyboard or a joystick.

        :type input_type_name: str
        :param input_type_name: It can be "keyboard" or "joystick".

        :type action_name: str
        :param action_name: The name used to identify the associated action.
        """

        if not self.waiting_input:
            self.config_sub_widget(
                ("commandButton", input_type_name, action_name), enable=False
            )
            self.waiting_input = (input_type_name, action_name)
