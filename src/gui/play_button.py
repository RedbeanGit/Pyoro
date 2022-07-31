# -*- coding:utf-8 -*-

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
Provide a Play_button class.

Created on 18/08/2018.
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH
from game.util import Game
from gui.button import Button


class PlayButton(Button):
    """
    Create a button displayed in the main menu to start a new game.
    """

    DEFAULT_KWARGS = {
        "background_anchor": (0, -0.05),
        "background_image": os.path.join(
            GUI_IMAGE_PATH, "play button {}", "play_button.png"
        ),
        "on_hover_background_image": os.path.join(
            GUI_IMAGE_PATH, "play button {}", "play_button_hover.png"
        ),
        "on_click_background_image": os.path.join(
            GUI_IMAGE_PATH, "play button {}", "play_button_click.png"
        ),
        "on_middle_click_background_image": os.path.join(
            GUI_IMAGE_PATH, "play button {}", "play_button_middle_click.png"
        ),
        "on_right_click_background_image": os.path.join(
            GUI_IMAGE_PATH, "play button {}", "play_button_right_click.png"
        ),
        "disable_background_image": os.path.join(
            GUI_IMAGE_PATH, "play button {}", "play_button_disable.png"
        ),
    }

    def __init__(self, activity, pos, game_id, **kwargs):
        """
        Initialize a new Play_button object.

        :type activity: gui.activity.Activity
        :param activity: The parent activity of this widget.

        :type pos: tuple
        :param pos: The default position of the button in a (x, y) tuple where
                x and y are integers.

        :type game_id: int
        :param game_id: The game to launch when clicked (0=Pyoro, 1=Pyoro 2).

        background_image, on_hover_background_image, on_click_background_image,
        on_middle_click_background_image, on_right_click_background_image and
        disable_background_image can be defined.
        """

        PlayButton.update_default_kwargs(kwargs)
        self.game_id = game_id
        Button.__init__(self, activity, pos, **kwargs)
        if self.kwargs["enable"]:
            self.config(
                text=f"High Score: {Game.options.get('high score', [0, 0])[game_id]}"
            )

    def load_background_images(self):
        """
        Load backgrounds by stretching the images associated to the give
                game_id.
        """

        back_names = (
            "background_image",
            "on_hover_background_image",
            "on_click_background_image",
            "on_middle_click_background_image",
            "on_right_click_background_image",
            "disable_background_image",
        )
        for back_name in back_names:
            if self.kwargs[back_name]:
                if "{}" in self.kwargs[back_name]:
                    self.kwargs[back_name] = self.kwargs[back_name].format(
                        self.game_id + 1
                    )
        Button.load_background_images(self)

    def on_end_click(self):
        """
        Launch the game.
        """

        if self.clicked:
            self.clicked = False
            if self.kwargs["on_click_fct"]:
                self.kwargs["on_click_fct"](
                    self.game_id,
                    *self.kwargs["on_click_args"],
                    **self.kwargs["on_click_kwargs"],
                )
