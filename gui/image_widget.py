# -*- coding: utf-8 -*-

"""
Provide a high level image object.

Created on 31/12/2018
"""

from gui.image_transformer import resizeImage
from gui.widget import Widget

__author__ = "Julien Dubois"
__version__ = "1.1.2"


class Image_widget(Widget):

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
