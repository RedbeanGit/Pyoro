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
Provide a widget to create a "Game over" menu.

Created on 21/08/2018
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH
from gui.clickable_text import ClickableText
from gui.menu_widget import MenuWidget
from gui.text import Text


class GameOverMenu(MenuWidget):
    """
    This class create a "Game over" menu widget displayed when Pyoro dies
    """

    DEFAULT_KWARGS = {"font_size": 20, "font": os.path.join(GUI_IMAGE_PATH, "font.ttf")}

    def __init__(self, activity, pos, score, quit_fct, **kwargs):
        """
        Initialise a new GameOverMenu object.

        :type activity: gui.activity.Activity
        :param activity: The parent activity of this widget.

        :type pos: tuple
        :param pos: The default position of the menu in a (x, y) tuple where
            x and y are integers.

        :type score: int
        :param score: The score at the of the game.

        :type quit_fct: callable
        :param quit_fct: A callable to run when the player click on the "Quit"
            button.
        """

        GameOverMenu.update_default_kwargs(kwargs)

        self.quit_fct = quit_fct
        self.score = score

        MenuWidget.__init__(self, activity, pos, **kwargs)

    def init_widgets(self):
        """
        Create subwidgets which will compose the menu.
        """

        width, height = self.kwargs["size"]
        font = self.kwargs["font"]
        font_size = self.kwargs["font_size"]
        font_size_medium = font_size - 3

        pos_x = int(width * 0.5)
        pos_y = int(height * 0.25)
        self.add_sub_widget(
            "titleText",
            Text,
            (pos_x, pos_y),
            "Game Over",
            anchor=(0, 0),
            font=font,
            font_size=font_size,
        )
        pos_y = int(height * 0.50)
        self.add_sub_widget(
            "scoreText",
            Text,
            (pos_x, pos_y),
            f"score : {self.score}",
            anchor=(0, 0),
            font=font,
            font_size=font_size_medium,
        )
        pos_y = int(height * 0.75)
        self.add_sub_widget(
            "quitClickableText",
            ClickableText,
            (pos_x, pos_y),
            "quitter",
            anchor=(0, 0),
            font=font,
            font_size=font_size_medium,
            on_click_fct=self.destroy,
        )

    def destroy(self):
        """
        Destroy the widget and call self.quit_fct.
        """

        MenuWidget.destroy(self)
        self.quit_fct()
