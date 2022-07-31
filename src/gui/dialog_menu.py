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
Provide a DialogMenu class.

Created on 30/10/2018.
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH
from gui.menu_widget import MenuWidget
from gui.clickable_text import ClickableText
from gui.text import Text


class DialogMenu(MenuWidget):
    """
    Create a menu to alert the player or to ask his opinion.
    """

    DEFAULT_KWARGS = {
        "font": os.path.join(GUI_IMAGE_PATH, "font.ttf"),
        "positive_args": (),
        "positive_kwargs": {},
        "negative_fct": None,
        "negative_args": (),
        "negative_kwargs": {},
        "description": "",
    }

    def __init__(self, activity, pos, message, positive_fct, **kwargs):
        """
        Initialize a new DialogMenu objects.

        :type activity: gui.activity.Activity
        :param activity: The parent activity of this widget.

        :type pos: tuple
        :param pos: The default position of the widget in a (x, y) tuple where
            x and y are integers.

        :type message: str
        :param message: A message to display to the player.

        :type positive_fct: callable
        :param positive_fct: A callable to call on click on the first button.

        font, positive_args, positive_kwargs, negative_fct, negative_args,
        negative_kwargs and description can be defined.

        If negative_fct is defined, a second button is created.
        """

        DialogMenu.update_default_kwargs(kwargs)

        self.message = message
        self.positive_fct = positive_fct

        MenuWidget.__init__(self, activity, pos, **kwargs)

    def init_widgets(self):
        """
        Create and initialize all subwidgets.
        """

        width, height = self.kwargs["size"]
        font = self.kwargs["font"]
        pos_x = int(width * 0.5)
        pos_y = int(height * 0.25)
        self.add_sub_widget(
            "titleText",
            Text,
            (pos_x, pos_y),
            self.message,
            font=font,
            font_size=22,
            anchor=(0, 0),
        )

        if self.kwargs["description"]:
            pos_x = int(width * 0.1)
            pos_y = int(height * 0.4)
            self.add_sub_widget(
                "descText",
                Text,
                (pos_x, pos_y),
                self.kwargs["description"],
                font=font,
                font_size=18,
                anchor=(-1, 0),
            )

        pos_y = int(height * 0.8)
        pos_x = int(width * 0.75)
        if self.kwargs["negative_fct"]:
            self.add_sub_widget(
                "positiveText",
                ClickableText,
                (pos_x, pos_y),
                "oui",
                font=font,
                font_size=18,
                anchor=(0, 0),
                on_click_fct=self.positive_action,
            )

            pos_x = int(width * 0.25)
            self.add_sub_widget(
                "negativeText",
                ClickableText,
                (pos_x, pos_y),
                "non",
                font=font,
                font_size=18,
                anchor=(0, 0),
                on_click_fct=self.negative_action,
            )
        else:
            self.add_sub_widget(
                "positiveText",
                ClickableText,
                (pos_x, pos_y),
                "ok",
                font=font,
                font_size=18,
                anchor=(0, 0),
                on_click_fct=self.positive_action,
            )

    def negative_action(self):
        """
        This method is called when the second button is clicked. It destroys
            the menu and call negative_fct.
        """

        self.destroy()
        self.kwargs["negative_fct"](
            *self.kwargs["negative_args"], **self.kwargs["negative_kwargs"]
        )

    def positive_action(self):
        """
        This method is called when the first button is clicked. It destroys
            the menu and call positive_fct.
        """
        self.destroy()
        self.positive_fct(
            *self.kwargs["positive_args"], **self.kwargs["positive_kwargs"]
        )
