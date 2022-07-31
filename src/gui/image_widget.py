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
Provide a high level image object.

Created on 31/12/2018
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from gui.image_transformer import resize_image
from gui.widget import Widget


class ImageWidget(Widget):
    """
    Create a widget used to render image easily.
    """

    DEFAULT_KWARGS = {}

    def __init__(self, activity, pos, image_path, **kwargs):
        """
        Initialize a new ImageWidget object.

        :type activity: gui.activity.Activity
        :param activity: The parent activity of this widget.

        :type pos: tuple
        :param pos: The position of the widget in a (x, y) tuple, where x and y
            are integers.

        :type image_path: str
        :param image_path: The image's filepath.
        """

        ImageWidget.update_default_kwargs(kwargs)
        self.activity = activity
        self.load_image(image_path)

        if "size" in kwargs:
            self.resize(kwargs["size"])
        else:
            kwargs["size"] = self.size

        Widget.__init__(self, activity, pos, **kwargs)

    def load_image(self, image_path):
        """
        Load an image file to this object.

        :type image_path: str
        :param image_path: The filepath to the image to load.
        """

        self.image = self.activity.window.get_image(image_path)
        self.size = self.image.get_size()

    def update(self, delta_time):
        """
        Redraw the image on the game window.
        This method should be called each frame.

        :type delta_time: float
        :param delta_time: Time elapsed since the last call of this method (in
            seconds)
        """
        self.activity.window.draw_image(self.image, self.get_real_pos())

    def resize(self, new_size):
        """
        Resize the widget by stretching the image.

        :type new_size: tuple
        :param new_size: The size to give to the widget in a (width, height)
            tuple, where width and height are integers.
        """

        self.image = resize_image(self.image, new_size)
        self.size = tuple(new_size)
