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
Provide a Clickable_text class used to create discreet buttons or links.

Created on 10/04/2018.
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from gui.eventable_widget import EventableWidget
from gui.text import Text


class ClickableText(Text, EventableWidget):
    """
    Create a text widget which will react on user events.
    """

    DEFAULT_KWARGS = {
        "on_click_text_color": (200, 200, 200, 255),
        "on_middle_click_text_color": (100, 100, 100, 255),
        "on_right_click_text_color": (220, 220, 220, 255),
        "on_hover_text_color": (230, 230, 230, 255),
        "disable_text_color": (240, 240, 240, 235),
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

        on_click_text_color, on_middle_click_text_color, on_right_click_text_color,
        on_hover_text_color, disable_text_color, can be defined.
        """

        ClickableText.update_default_kwargs(kwargs)
        Text.__init__(self, activity, pos, text, **kwargs)
        EventableWidget.__init__(self, activity, pos, **self.kwargs)

    def update(self, delta_time):
        """
        Update the clickable text by redrawing it on the window with the
            appropriate color.

        :type delta_time: float
        :param delta_time: Time elapsed since the last call of this method (in
            seconds).
        """

        if not self.kwargs["enable"]:
            self.font.fgcolor = self.kwargs["disable_text_color"]
        elif self.clicked:
            self.font.fgcolor = self.kwargs["on_click_text_color"]
        elif self.right_clicked:
            self.font.fgcolor = self.kwargs["on_right_click_text_color"]
        elif self.middle_clicked:
            self.font.fgcolor = self.kwargs["on_middle_click_text_color"]
        elif self.hovered:
            self.font.fgcolor = self.kwargs["on_hover_text_color"]
        else:
            self.font.fgcolor = self.kwargs["text_color"]
        Text.update(self, delta_time)
