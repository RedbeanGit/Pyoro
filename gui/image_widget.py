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

from gui.image_transformer import resizeImage
from gui.widget import Widget


class Image_widget(Widget):
    """
    Create a widget used to render image easily.
    """

    DEFAULT_KWARGS = {

    }

    def __init__(self, activity, pos, imagePath, **kwargs):
        """
        Initialize a new Image_widget object.

        :type activity: gui.activity.Activity
        :param activity: The parent activity of this widget.

        :type pos: tuple
        :param pos: The position of the widget in a (x, y) tuple, where x and y
            are integers.

        :type imagePath: str
        :param imagePath: The image's filepath.
        """

        Image_widget.updateDefaultKwargs(kwargs)
        self.activity = activity
        self.loadImage(imagePath)

        if "size" in kwargs:
            self.resize(kwargs["size"])
        else:
            kwargs["size"] = self.size

        Widget.__init__(self, activity, pos, **kwargs)

    def loadImage(self, imagePath):
        """
        Load an image file to this object.

        :type imagePath: str
        :param imagePath: The filepath to the image to load.
        """

        self.image = self.activity.window.getImage(imagePath)
        self.size = self.image.get_size()

    def update(self, deltaTime):
        """
        Redraw the image on the game window.
        This method should be called each frame.

        :type deltaTime: float
        :param deltaTime: Time elapsed since the last call of this method (in
            seconds)
        """
        self.activity.window.drawImage(self.image, self.getRealPos())

    def resize(self, newSize):
        """
        Resize the widget by stretching the image.

        :type newSize: tuple
        :param newSize: The size to give to the widget in a (width, height)
            tuple, where width and height are integers.
        """

        self.image = resizeImage(self.image, newSize)
        self.size = tuple(newSize)
