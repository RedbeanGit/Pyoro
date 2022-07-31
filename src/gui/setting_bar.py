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
Provide a SettingBar class.

Created on 20/08/2018.
"""

import os
from pygame.locals import MOUSEMOTION

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH
from gui.eventable_widget import EventableWidget
from gui.image_transformer import stretch_image


class SettingBar(EventableWidget):
    """
    Create a widget allowing the player to choose an approximate value
        within [0; 1].
    """

    DEFAULT_KWARGS = {
        "line_thickness": 16,
        "cursor_width": 16,
        "line_image_border_size": 4,
        "cursor_image_border_size": 4,
        "value": 0,
        "line_image": os.path.join(GUI_IMAGE_PATH, "setting bar", "line.png"),
        "on_hover_line_image": os.path.join(
            GUI_IMAGE_PATH, "setting bar", "line_hover.png"
        ),
        "on_click_line_image": os.path.join(
            GUI_IMAGE_PATH, "setting bar", "line_click.png"
        ),
        "on_middle_click_line_image": os.path.join(
            GUI_IMAGE_PATH, "setting bar", "line_middle_click.png"
        ),
        "on_right_click_line_image": os.path.join(
            GUI_IMAGE_PATH, "setting bar", "line_right_click.png"
        ),
        "disable_line_image": os.path.join(
            GUI_IMAGE_PATH, "setting bar", "line_disable.png"
        ),
        "cursor_image": os.path.join(GUI_IMAGE_PATH, "setting bar", "cursor.png"),
        "on_hover_cursor_image": os.path.join(
            GUI_IMAGE_PATH, "setting bar", "cursor_hover.png"
        ),
        "on_click_cursor_image": os.path.join(
            GUI_IMAGE_PATH, "setting bar", "cursor_click.png"
        ),
        "on_middle_click_cursor_image": os.path.join(
            GUI_IMAGE_PATH, "setting bar", "cursor_middle_click.png"
        ),
        "on_right_click_cursor_image": os.path.join(
            GUI_IMAGE_PATH, "setting bar", "cursor_right_click.png"
        ),
        "disable_cursor_image": os.path.join(
            GUI_IMAGE_PATH, "setting bar", "cursor_disable.png"
        ),
    }

    def __init__(self, activity, pos, **kwargs):
        """
        Initialize a new Text objects.

        :type activity: gui.activity.Activity
        :param activity: The parent activity of this widget.

        :type pos: tuple
        :param pos: The default position of the widget in a (x, y) tuple where
            x and y are integers.

        line_thickness, cursor_width, line_image_border_size,
        cursor_image_border_size, value, line_image, on_hover_line_image,
        on_click_line_image, on_middle_click_line_image, on_right_click_line_image,
        disable_line_image, cursor_image, on_hover_cursor_image,
        on_middle_click_cursor_image, on_right_click_cursor_image and
        disable_cursor_image can be defined.
        """

        SettingBar.update_default_kwargs(kwargs)
        EventableWidget.__init__(self, activity, pos, **kwargs)

        self.line_image = None
        self.on_hover_line_image = None
        self.on_click_line_image = None
        self.on_middle_click_line_image = None
        self.on_right_click_line_image = None
        self.disable_line_image = None

        self.cursor_image = None
        self.on_hover_cursor_image = None
        self.on_click_cursor_image = None
        self.on_middle_click_cursor_image = None
        self.on_right_click_cursor_image = None
        self.disable_cursor_image = None

        self.cursor_pos = self.get_cursor_pos_with_value(self.kwargs["value"])

        self.loadline_images()
        self.load_cursor_images()

    def loadline_images(self):
        """
        Load the line images and stretch them to the right size.
        """

        image_names = (
            "line_image",
            "on_hover_line_image",
            "on_click_line_image",
            "on_middle_click_line_image",
            "on_right_click_line_image",
            "disable_line_image",
        )

        for image_name in image_names:
            if self.kwargs[image_name]:
                image = stretch_image(
                    self.activity.window.get_image(self.kwargs[image_name]),
                    (self.kwargs["size"][0], self.kwargs["line_thickness"]),
                    self.kwargs["line_image_border_size"],
                )
                setattr(self, image_name, image)

    def load_cursor_images(self):
        """
        Load the cursor images and stretch them to the right size.
        """

        image_names = (
            "cursor_image",
            "on_hover_cursor_image",
            "on_click_cursor_image",
            "on_middle_click_cursor_image",
            "on_right_click_cursor_image",
            "disable_cursor_image",
        )

        for image_name in image_names:
            if self.kwargs[image_name]:
                image = stretch_image(
                    self.activity.window.get_image(self.kwargs[image_name]),
                    (self.kwargs["cursor_width"], self.kwargs["size"][1]),
                    self.kwargs["cursor_image_border_size"],
                )
                setattr(self, image_name, image)

    def update(self, delta_time):
        """
        Draw the line and the cursor.

        :type delta_time: float
        :param delta_time: Time elapsed since the last call of this method (in
            seconds).
        """

        self.draw_line()
        self.draw_cursor()

    def draw_line(self):
        """
        Draw the right line image according to the widget state.
        """

        if not self.kwargs["enable"] and self.disable_line_image:
            self.activity.window.draw_image(
                self.disable_line_image, self.get_line_pos()
            )

        if self.clicked and self.on_click_line_image:
            self.activity.window.draw_image(
                self.on_click_line_image, self.get_line_pos()
            )

        elif self.right_clicked and self.on_right_click_line_image:
            self.activity.window.draw_image(
                self.on_right_click_line_image, self.get_line_pos()
            )

        elif self.middle_clicked and self.on_middle_click_line_image:
            self.activity.window.draw_image(
                self.on_middle_click_line_image, self.get_line_pos()
            )

        elif self.hovered and self.on_hover_line_image:
            self.activity.window.draw_image(
                self.on_hover_line_image, self.get_line_pos()
            )

        elif self.line_image:
            self.activity.window.draw_image(self.line_image, self.get_line_pos())

    def draw_cursor(self):
        """
        Draw the right line image according to the widget state.
        """

        if not self.kwargs["enable"] and self.disable_cursor_image:
            self.activity.window.draw_image(
                self.disable_cursor_image, self.get_cursor_pos()
            )

        if self.clicked and self.on_click_cursor_image:
            self.activity.window.draw_image(
                self.on_click_cursor_image, self.get_cursor_pos()
            )

        elif self.right_clicked and self.on_right_click_cursor_image:
            self.activity.window.draw_image(
                self.on_right_click_cursor_image, self.get_cursor_pos()
            )

        elif self.middle_clicked and self.on_middle_click_cursor_image:
            self.activity.window.draw_image(
                self.on_middle_click_cursor_image, self.get_cursor_pos()
            )

        elif self.hovered and self.on_hover_cursor_image:
            self.activity.window.draw_image(
                self.on_hover_cursor_image, self.get_cursor_pos()
            )

        elif self.cursor_image:
            self.activity.window.draw_image(self.cursor_image, self.get_cursor_pos())

    def get_line_pos(self):
        """
        Compute the position of the upper left corner of the line.

        :rtype: list
        :returns: A [x, y] list where x and y are both integers.
        """

        real_pos = self.get_real_pos()
        return [
            real_pos[0],
            real_pos[1]
            + self.kwargs["size"][1] // 2
            - self.kwargs["line_thickness"] // 2,
        ]

    def get_cursor_pos(self):
        """
        Compute the position of the upper left corner of the cursor.

        :rtype: list
        :returns: A [x, y] list where x and y are both integers.
        """

        real_pos = self.get_real_pos()
        return [self.cursor_pos - self.kwargs["cursor_width"] // 2, real_pos[1]]

    def on_event(self, event):
        """
        This method is called on all user events detected by Pygame.

        :type event: pygame.event.Event
        :param event: The event to handle.
        """

        EventableWidget.on_event(self, event)
        if self.kwargs["enable"] and self.clicked:
            if event.type == MOUSEMOTION:
                real_pos = self.get_real_pos()

                if (
                    event.pos[0] >= real_pos[0] + self.kwargs["cursor_width"] / 2
                    and event.pos[0]
                    <= real_pos[0]
                    + self.kwargs["size"][0]
                    - self.kwargs["cursor_width"] / 2
                ):
                    self.cursor_pos = event.pos[0]

                elif event.pos[0] < real_pos[0] + self.kwargs["cursor_width"] / 2:
                    self.cursor_pos = real_pos[0] + self.kwargs["cursor_width"] / 2

                else:
                    self.cursor_pos = (
                        real_pos[0]
                        + self.kwargs["size"][0]
                        - self.kwargs["cursor_width"] / 2
                    )

    def get_value(self):
        """
        Return a value between 0 and 1 from the position of the cursor on the
            line.

        :rtype: float
        :returns: The value of the setting bar.
        """

        real_pos = self.get_real_pos()
        if self.kwargs["size"][0] - self.kwargs["cursor_width"] != 0:
            return (self.cursor_pos - real_pos[0] - self.kwargs["cursor_width"] / 2) / (
                self.kwargs["size"][0] - self.kwargs["cursor_width"]
            )
        return 0.5

    def get_cursor_pos_with_value(self, value):
        """
        Return the horizontal position of the upper left corner of the cursor
            from a give value.

        :type value: float
        :param value: Any float number between 0 and 1.

        :rtype: float
        :returns: The absolute x position of the cursor.
        """

        return (
            value * (self.kwargs["size"][0] - self.kwargs["cursor_width"])
            + self.kwargs["cursor_width"] / 2
            + self.get_real_pos()[0]
        )

    def config(self, **kwargs):
        """
        Change some kwargs of the widget (cursor_width, cursor_image, ...).
        """

        EventableWidget.config(self, **kwargs)

        if (
            "cursor_image_border_size" in kwargs
            or "cursor_width" in kwargs
            or "cursor_image" in kwargs
            or "on_hover_cursor_image" in kwargs
            or "on_click_cursor_image" in kwargs
            or "on_middle_click_cursor_image" in kwargs
            or "on_right_click_cursor_image" in kwargs
            or "disable_cursor_image" in kwargs
        ):
            self.load_cursor_images()

        if (
            "line_image_border_size" in kwargs
            or "line_thickness" in kwargs
            or "line_image" in kwargs
            or "on_hover_line_image" in kwargs
            or "on_click_line_image" in kwargs
            or "on_middle_click_line_image" in kwargs
            or "on_right_click_line_image" in kwargs
            or "disable_line_image" in kwargs
        ):
            self.loadline_images()

        if "value" in kwargs:
            self.cursor_pos = self.get_cursor_pos_with_value(kwargs["value"])
