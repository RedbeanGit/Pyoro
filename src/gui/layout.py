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
Provide a class to manage widget dispositions, according to the screen
resolution.

Created on 16/12/2018
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.util import (
    get_layout_template,
    get_screen_ratio,
    get_screen_size,
    get_monitor_size,
)


class Layout:
    """
    Layout help to get widgets size, position and anchor according to
    the window resolution.
    """

    def __init__(self, window):
        """
        Initialize a ne Layout object.

        :type window: gui.window.Window
        :param window: A game window to work with.
        """

        self.window = window
        self.width = 1
        self.height = 1
        self.width_mm = 1
        self.height_mm = 1
        self.dpm = 1
        self.template = {}

    def load(self):
        """
        Try to load a layout template adapted to a defined resolution.

        :type width: int
        :param width: (Optional) The width of the window (in pixel). Leave
            None to use	the current window width.

        :type height: int
        :param height: (Optional) The height of the window (in pixel). Leave
            None to use the current window height.
        """

        self.width, self.height = get_screen_size()
        self.width_mm, self.height_mm = get_monitor_size()
        self.dpm = (self.width / self.width_mm + self.height / self.height_mm) / 2
        self.template = get_layout_template(get_screen_ratio())

    def get_widget_pos(self, widget_name):
        """
        Return the absolute position of a widget, in pixel.

        :type widget_name: str
        :param widget_name: A string representing a widget.

        :rtype: tuple
        :returns: (x, y) coordinates referencing the widget position.
            If something wrong happen, return (0, 0)
        """

        width, height = self.get_widget_info(widget_name, "pos", [0, 0])
        return int(width * self.width / 100), int(height * self.height / 100)

    def get_widget_size(self, widget_name):
        """
        Return the size of a widget, in pixel.

        :type widget_name: str
        :param widget_name: A string representing a widget.

        :rtype: tuple
        :returns: (w, h) tuple referencing the widget size.
        """

        min_width_mm, min_height_mm = self.get_widget_info(
            widget_name, "min_mm_format", [0, 0]
        )
        width_mm, height_mm = self.get_widget_info(widget_name, "size_mm", [1, 1])
        width_pixel, height_pixel = self.get_widget_info(widget_name, "size", [1, 1])
        width, height = width_pixel * self.width / 100, height_pixel * self.height / 100

        if self.width_mm >= min_width_mm:
            width = width_mm * self.dpm

        if self.height_mm >= min_height_mm:
            height = height_mm * self.dpm

        return int(width), int(height)

    def get_widget_anchor(self, widget_name):
        """
        Return the anchor position of a widget.

        :type widget_name: str
        :param widget_name: A string representing a widget.

        :rtype: tuple
        :returns: (x, y) coordinates referencing the widget anchor point,
            relative to the widget position. If something wrong happen,
            return (0, 0).
        """

        return self.get_widget_info(widget_name, "anchor", [0, 0])

    def get_font_size(self, widget_name):
        """
        Return the font size of a text widget.

        :type widget_name: str
        :param widget_name: A string representing a text widget.

        :rtype: int
        :returns: The font size in pixel.
        """

        min_width_mm, min_height_mm = self.get_widget_info(
            widget_name, "min_mm_format", [0, 0]
        )
        font_mm = self.get_widget_info(widget_name, "font_size_mm", 1)
        font_pixel = self.get_widget_info(widget_name, "font_size", 1)

        if self.height_mm < min_height_mm or self.width_mm < min_width_mm:
            return int(font_pixel * (self.height + self.width) / 200)
        return int(font_mm * self.dpm)

    def get_widget_info(self, widget_name, info, default_value=None):
        """
        Return an information for a given widget.

        :type widget_name: str
        :param widget_name: A string representing a widget.

        :type info: str
        :param info: The name of info searched.

        :type default_value: object
        :param default_value: (Optional). The returned value if something wrong
            happen.

        :Example: layout.get_widget_info("play_button_1", "size", [1, 1])
        """

        if widget_name in self.template:
            if info in self.template[widget_name]:
                return self.template[widget_name][info]
            print(
                "[WARNING] [Layout.get_widget_info] No info "
                + f'"{info}" for "{widget_name}"'
            )
        else:
            print(f'[WARNING] [Layout.get_widget_info] No widget "{widget_name}" found')
        return default_value
