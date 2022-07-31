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
Provide a class to create button widgets with update on click and on hover.

Created on 18/08/2018
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH

from gui.eventable_widget import EventableWidget
from gui.image_transformer import resize_image
from gui.text import Text


class Button(EventableWidget):
    """
    A simple button widget.
    """

    DEFAULT_KWARGS = {
        "text": "",
        "text_kwargs": {"anchor": (0, 0)},
        "text_anchor": (0, 0),
        "background_image": os.path.join(GUI_IMAGE_PATH, "button", "button.png"),
        "on_hover_background_image": os.path.join(
            GUI_IMAGE_PATH, "button", "button_hover.png"
        ),
        "on_click_background_image": os.path.join(
            GUI_IMAGE_PATH, "button", "button_click.png"
        ),
        "on_middle_click_background_image": os.path.join(
            GUI_IMAGE_PATH, "button", "button_middle_click.png"
        ),
        "on_right_click_background_image": os.path.join(
            GUI_IMAGE_PATH, "button", "button_right_click.png"
        ),
        "disable_background_image": os.path.join(
            GUI_IMAGE_PATH, "button", "button_disable.png"
        ),
    }

    def __init__(self, activity, pos, **kwargs):
        """
        Initialize a new Button object.

        :type activity: gui.activity.Activity
        :param activity: The parent activity of this widget.

        :type pos: tuple
        :param pos: The default position of the button in a (x, y) tuple where
            x and y are integers.

        text, text_kwargs, text_anchor, background_image, on_hover_background_image,
        on_click_background_image, on_middle_click_background_image,
        on_right_click_background_image and disable_background_image can be defined.
        """

        Button.update_default_kwargs(kwargs)
        Button.update_default_text_kwargs(kwargs)
        EventableWidget.__init__(self, activity, pos, **kwargs)
        self.background_images = {}
        self.text = Text(
            self.activity,
            self.get_text_pos(),
            self.kwargs["text"],
            **self.kwargs["text_kwargs"]
        )
        self.load_background_images()

    @classmethod
    def update_default_text_kwargs(cls, kwargs):
        """
        Add missing optional text kwargs with
            Button.DEFAULT_KWARGS["text_kwargs"].

        :type kwargs: dict
        :param kwargs: A {kwargsName: value} dictionnary to update with
            missing kwargs.
        """

        for key, value in cls.DEFAULT_KWARGS["text_kwargs"].items():
            if key not in kwargs["text_kwargs"]:
                kwargs["text_kwargs"][key] = value

    def load_background_images(self):
        """
        Load the button background images.
        """

        event_names = (
            "",
            "on_hover",
            "on_click",
            "on_middle_click",
            "on_right_click",
            "disable",
        )

        for event_name in event_names:
            if event_name:
                background_name = event_name + "_background_image"
            else:
                background_name = "background_image"
            self.background_images[event_name] = resize_image(
                self.activity.window.get_image(self.kwargs[background_name]),
                self.kwargs["size"],
            )

    def update(self, delta_time):
        """
        Redraw the button with the best background for the current event.

        :type delta_time: float
        :param delta_time: Time elapsed since the last call of this method (in
            seconds).
        """

        event_name = ""
        if not self.kwargs["enable"]:
            event_name = "disable"
        elif self.clicked:
            event_name = "on_click"
        elif self.right_clicked:
            event_name = "on_right_click"
        elif self.middle_clicked:
            event_name = "on_middle_click"
        elif self.hovered:
            event_name = "on_hover"

        if event_name in self.background_images:
            self.activity.window.draw_image(
                self.background_images[event_name], self.get_real_pos()
            )

        self.text.update(delta_time)
        EventableWidget.update(self, delta_time)

    def config(self, **kwargs):
        """
        Change some attributes of this button and update it.
        """

        EventableWidget.config(self, **kwargs)
        if "text" in kwargs:
            self.text.text = kwargs["text"]
        if "text_anchor" in kwargs:
            self.text.pos = self.get_text_pos()
        if "text_kwargs" in kwargs:
            self.text.config(**kwargs["text_kwargs"])

        # If any background is modified
        if (
            "background_image" in kwargs
            or "on_hover_background_image" in kwargs
            or "on_click_background_image" in kwargs
            or "on_middle_click_background_image" in kwargs
            or "on_right_click_background_image" in kwargs
            or "disable_background_image" in kwargs
        ):
            self.load_background_images()

    def get_text_pos(self):
        """
        Return the text position according to this button pos.

        :rtype: tuple
        :returns: The central position of the text in an (x, y) tuple where x
            and y are both integers.
        """

        pos_x, pos_y = self.get_real_pos()
        width, height = self.kwargs["size"]
        anchor_x, anchor_y = self.kwargs["text_anchor"]
        return (pos_x + width * (anchor_x + 1) / 2, pos_y + height * (anchor_y + 1) / 2)
