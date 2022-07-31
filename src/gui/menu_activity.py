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
Provide an activity to manage the main menu.

Created on 10/04/2018
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH
from game.util import Game

from gui.activity import Activity
from gui.button import Button
from gui.image_widget import ImageWidget
from gui.level_drawer import LevelDrawer
from gui.play_button import PlayButton
from gui.option_menu import OptionMenu


class MenuActivity(Activity):
    """
    Layout managing the menu's components
    """

    def __init__(self, window, game_id):
        """
        Initialize a new Menu_activity object.

        :type window: gui.window.Window
        :param window: The parent game window.

        :type game_id: int
        :param game_id: The game_id of the level in background.
                0 = Pyoro, 1 = Pyoro 2.
        """

        Activity.__init__(self, window)
        self.level_drawer = LevelDrawer(self, game_id, bot_mode=True)

    def init_sounds(self):
        """
        Reference the "intro.wav" music and start to play it.
        This method reset the global Audio_player speed.
        """

        self.__init_sounds__(
            ("intro",), os.path.join("data", "audio", "musics"), "music"
        )
        Game.audio_player.set_speed(1)
        self.sounds["intro"].play(-1)

    def init_widgets(self):
        """
        Create widgets (Play, option and quit buttons).
        """

        widget_infos = {
            "title_image": {
                "type": ImageWidget,
                "args": (os.path.join(GUI_IMAGE_PATH, "title.png"),),
                "kwargs": {},
            },
            "play_button_1": {
                "type": PlayButton,
                "args": (0,),
                "kwargs": {
                    "on_click_fct": self.window.set_game_render,
                    "text_anchor": (0, -0.1),
                },
            },
            "play_button_2": {
                "type": PlayButton,
                "args": (1,),
                "kwargs": {
                    "on_click_fct": self.window.set_game_render,
                    "enable": self.is_pyoro_2_unlocked(),
                    "text_anchor": (0, -0.1),
                },
            },
            "option_button": {
                "type": Button,
                "args": (),
                "kwargs": {"text": "Options", "on_click_fct": self.create_option_menu},
            },
            "quit_button": {
                "type": Button,
                "args": (),
                "kwargs": {"text": "Quitter", "on_click_fct": self.window.destroy},
            },
        }

        for widget_name, kwargs in widget_infos.items():
            pos = self.layout.get_widget_pos(widget_name)
            size = self.layout.get_widget_size(widget_name)
            anchor = self.layout.get_widget_anchor(widget_name)
            fsize = self.layout.get_font_size(widget_name)

            self.add_widget(
                widget_name,
                kwargs["type"],
                pos,
                *kwargs["args"],
                size=size,
                anchor=anchor,
                textKwargs={"font_size": fsize},
                **kwargs["kwargs"]
            )

    def create_option_menu(self):
        """
        Display an option menu.
        """

        size = self.layout.get_widget_size("option_menu")
        pos = self.layout.get_widget_pos("option_menu")
        anchor = self.layout.get_widget_anchor("option_menu")
        fsize = self.layout.get_font_size("option_menu")

        self.add_widget(
            "option_menu",
            OptionMenu,
            pos,
            self.on_option_menu_destroy,
            size=size,
            anchor=anchor,
            font_size=fsize,
        )

    def on_option_menu_destroy(self):
        """
        This method is called when the option menu is destroyed.
        Remove the option menu from the updatable widgets list.
        """

        self.widgets["play_button_2"].config(enable=self.is_pyoro_2_unlocked())
        self.remove_widget("option_menu")

    def update(self, delta_time):
        """
        Update the level and redraw graphical components.

        :type delta_time: float
        :param delta_time: Time elapsed since the last call of this method
                (in seconds).
        """

        self.level_drawer.update(delta_time)
        Activity.update(self, delta_time)

    def is_pyoro_2_unlocked(self):
        """
        Check if Pyoro 2 is unlocked. To unlock Pyoro 2, the score must be
                greater than 10000.

        :rtype: bool
        :returns: True if Pyoro 2 is unlocked, otherwise False.
        """

        high_score = Game.options.get("high score", [0, 0])
        return high_score[0] >= 10000
