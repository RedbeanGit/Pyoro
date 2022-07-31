# -*- coding: utf-8 -*-

#   This file is part of Pyoro (A Python fan game).
#
#   Metawars is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Metawars is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
Provide a Text class widget.

Created on 29/03/2018.
"""

import os
import pygame.freetype

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH
from gui.widget import Widget


class Text(Widget):
    """
    Create a widget used to render text.
    """

    DEFAULT_KWARGS = {
        "font_size": 20,
        "font": os.path.join(GUI_IMAGE_PATH, "font.ttf"),

        "bold": False,
        "wide": False,
        "italic": False,
        "underline": False,
        "vertical_mode": False,

        "text_color": (255, 255, 255, 255),
        "background_color": None
    }

    def __init__(self, activity, pos, text, **kwargs):
        """
        Initialize a new Text objects.

        :type activity: gui.activity.Activity
        :param activity: The parent activity of this widget.

        :type pos: tuple
        :param pos: The default position of the widget in a (x, y) tuple where
            x and y are integers.

        :type text: str
        :param text: The text to render.

        font, font_size, bold, wide, italic, underline, vertical_mode, 
        text_color, and background_color can be defined.
        """

        Text.update_default_kwargs(kwargs)
        Widget.__init__(self, activity, pos, **kwargs)
        self.text = text
        self.create_font()

    def create_font(self):
        """
        Load the font used to render the text.
        """

        self.font = pygame.freetype.Font(self.kwargs["font"])
        kwargs = dict(self.kwargs)
        kwargs.pop("font")
        self.config(**kwargs)

    def update(self, delta_time):
        """
        Update the text by drawing it on the window.

        :type delta_time: float
        :param delta_time: Time elapsed since the last call of this method (in
            seconds).
        """

        surface, rect = self.font.render(
            self.text, bgcolor=self.kwargs["background_color"])
        self.kwargs["size"] = [rect.width, rect.height]
        self.activity.window.draw_image(surface, self.get_real_pos())
        Widget.update(self, delta_time)

    def config(self, **kwargs):
        """
        Change some kwargs of the widget (font, font_size, bold, ...).
        """

        Widget.config(self, **kwargs)
        if "font" in kwargs:
            self.create_font()
        else:
            if "font_size" in kwargs:
                self.font.size = kwargs["font_size"]
            if "bold" in kwargs:
                self.font.strong = kwargs["bold"]
            if "wide" in kwargs:
                self.font.wide = kwargs["wide"]
            if "italic" in kwargs:
                self.font.oblique = kwargs["italic"]
            if "underline" in kwargs:
                self.font.underline = kwargs["underline"]
            if "vertical_mode" in kwargs:
                self.font.vertical = kwargs["vertical_mode"]
            if "text_color" in kwargs:
                self.font.fgcolor = kwargs["text_color"]
