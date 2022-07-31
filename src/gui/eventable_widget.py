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
Provide an EventableWidget base class to manage user events and inputs.

Created on 17/08/2018.
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from gui.widget import Widget


class EventableWidget(Widget):
    """
    This class exists to be subclassed by widgets which have to be able to
        handle user events.
    """

    DEFAULT_KWARGS = {
        "enable": True,
        "on_click_fct": None,
        "on_click_args": (),
        "on_click_kwargs": {},
        "on_hover_fct": None,
        "on_hover_args": (),
        "on_hover_kwargs": {},
        "on_middle_click_fct": None,
        "on_middle_click_args": (),
        "on_middle_click_kwargs": {},
        "on_right_click_fct": None,
        "on_right_click_args": (),
        "on_right_click_kwargs": {},
        "on_wheel_fct": None,
        "on_wheel_args": (),
        "on_wheel_kwargs": {},
        "on_click_sound": os.path.join("data", "audio", "sounds", "widget_click.wav"),
    }

    def __init__(self, activity, pos, **kwargs):
        """
        Initialize a new Button object.

        :type activity: gui.activity.Activity
        :param activity: The parent activity of this widget.

        :type pos: tuple
        :param pos: The default position of the widget in a (x, y) tuple where
            x and y are integers.

        on_click_fct, on_click_args, on_click_kwargs,
        on_hover_fct, on_hover_args, on_hover_kwargs,
        on_middle_click_fct, on_middle_click_args, on_middle_click_kwargs,
        on_right_click_fct, on_right_click_args, on_right_click_kwargs,
        on_wheel_fct, on_wheel_args, on_wheel_kwargs,
        and on_click_sound can be defined.
        """

        EventableWidget.update_default_kwargs(kwargs)
        Widget.__init__(self, activity, pos, **kwargs)
        self.hovered = False
        self.clicked = False
        self.middle_clicked = False
        self.right_clicked = False
        self.uneventable_zones = []
        self.on_click_sound = None

    def on_event(self, event):
        """
        This method is called on all user events detected by Pygame.

        :type event: pygame.event.Event
        :param event: The event to handle.
        """

        if self.kwargs["enable"]:
            if event.type == MOUSEMOTION:
                if not self.is_in_uneventable_zone(event.pos):
                    if self.is_in_widget(event.pos):
                        self.on_hover()
                    else:
                        self.on_end_hover()

            elif event.type == MOUSEBUTTONDOWN:
                if not self.is_in_uneventable_zone(event.pos):
                    if self.is_in_widget(event.pos):
                        if event.button == 1:
                            self.on_click()
                        elif event.button == 2:
                            self.on_middle_click()
                        elif event.button == 3:
                            self.on_right_click()
                        elif event.button == 4:
                            self.on_mouse_wheel(1)
                        elif event.button == 5:
                            self.on_mouse_wheel(-1)
                    else:
                        if event.button == 1:
                            self.on_click_out()
                        elif event.button == 2:
                            self.on_middle_click_out()
                        elif event.button == 3:
                            self.on_right_click_out()
                        elif event.button == 4:
                            self.on_mouse_wheel_out(1)
                        elif event.button == 5:
                            self.on_mouse_wheel_out(-1)

            elif event.type == MOUSEBUTTONUP:
                if not self.is_in_uneventable_zone(event.pos):
                    if self.is_in_widget(event.pos):
                        if event.button == 1:
                            self.on_end_click()
                        elif event.button == 2:
                            self.on_end_middle_click()
                        elif event.button == 3:
                            self.on_end_right_click()
                        elif event.button == 4:
                            self.on_end_mouse_wheel(1)
                        elif event.button == 5:
                            self.on_end_mouse_wheel(-1)
                    else:
                        if event.button == 1:
                            self.on_end_click_out()
                        elif event.button == 2:
                            self.on_end_middle_click_out()
                        elif event.button == 3:
                            self.on_end_right_click_out()
                        elif event.button == 4:
                            self.on_end_mouse_wheel_out(1)
                        elif event.button == 5:
                            self.on_end_mouse_wheel_out(-1)

    def on_hover(self):
        """
        Set hovered state to True and call on_hover_fct.
        """

        self.hovered = True
        if self.kwargs["on_hover_fct"]:
            self.kwargs["on_hover_fct"](
                *self.kwargs["on_hover_args"], **self.kwargs["on_hover_kwargs"]
            )

    def on_end_hover(self):
        """
        Set hovered state to False.
        """

        self.hovered = False

    def on_click(self):
        """
        Set clicked state to True.
        """

        self.clicked = True

    def on_middle_click(self):
        """
        Set middle_clicked state to True.
        """

        self.middle_clicked = True

    def on_right_click(self):
        """
        Set right_clicked state to True.
        """

        self.right_clicked = True

    def on_mouse_wheel(self, direction):
        """
        Call on_wheel_fct.
        """

        if self.kwargs["on_wheel_fct"]:
            self.kwargs["on_wheel_fct"](
                direction,
                *self.kwargs["on_wheel_args"],
                **self.kwargs["on_wheel_kwargs"]
            )

    def on_click_out(self):
        """
        Do nothing by default. This method has to be overridden.
        """

    def on_middle_click_out(self):
        """
        Do nothing by default. This method has to be overridden.
        """

    def on_right_click_out(self):
        """
        Do nothing by default. This method has to be overridden.
        """

    def on_mouse_wheel_out(self, direction):
        """
        Do nothing by default. This method has to be overridden.
        """

    def on_end_click(self):
        """
        Set clicked state to False and call on_click_fct.
        """

        if self.clicked:
            self.clicked = False
            if self.kwargs["on_click_fct"]:
                self.kwargs["on_click_fct"](
                    *self.kwargs["on_click_args"], **self.kwargs["on_click_kwargs"]
                )

    def on_end_middle_click(self):
        """
        Set middle_clicked state to False and call on_middle_click_fct.
        """

        if self.middle_clicked:
            self.middle_clicked = False
            if self.kwargs["on_middle_click_fct"]:
                self.kwargs["on_middle_click_fct"](
                    *self.kwargs["on_middle_click_args"],
                    **self.kwargs["on_middle_click_kwargs"]
                )

    def on_end_right_click(self):
        """
        Set right_clicked state to False and call on_right_click_fct.
        """

        if self.right_clicked:
            self.right_clicked = False
            if self.kwargs["on_right_click_fct"]:
                self.kwargs["on_right_click_fct"](
                    *self.kwargs["on_right_click_args"],
                    **self.kwargs["on_right_click_kwargs"]
                )

    def on_end_mouse_wheel(self, direction):
        """
        Do nothing by default. This method has to be overridden.
        """

    def on_end_click_out(self):
        """
        Set clicked state to False.
        """

        if self.clicked:
            self.clicked = False

    def on_end_middle_click_out(self):
        """
        Set middle_clicked state to False.
        """

        if self.middle_clicked:
            self.middle_clicked = False

    def on_end_right_click_out(self):
        """
        Set right_clicked state to False.
        """

        if self.right_clicked:
            self.right_clicked = False

    def on_end_mouse_wheel_out(self, direction):
        """
        Do nothing by default. This method has to be overridden.
        """

    def add_uneventable_zone(self, pos, size):
        """
        Add a zone where mouse events will have no effects for this widget.

        :type pos: tuple
        :param pos: A (x, y) tuple representing the top left corner of the
            uneventable zone (in pixel).

        :type size: tuple
        :param size: A (w, h) tuple representing the size in pixel of the
            uneventable zone.

        :rtype: tuple
        :returns: A (x, y, w, h) tuple representing the uneventable zone
            created.
        """

        real_pos = self.get_real_pos()

        if (
            pos[0] >= real_pos[0]
            and pos[0] <= real_pos[0] + self.kwargs["size"][0]
            and pos[1] >= real_pos[1]
            and pos[1] <= real_pos[1] + self.kwargs["size"][1]
        ):
            if pos[0] + size[0] > real_pos[0] + self.kwargs["size"][0]:
                size[0] = real_pos[0] + self.kwargs["size"][0] - pos[0]
            if pos[1] + size[1] > real_pos[1] + self.kwargs["size"][1]:
                size[1] = real_pos[1] + self.kwargs["size"][1] - pos[1]

            self.uneventable_zones.append((pos[0], pos[1], size[0], size[1]))

            return (pos[0], pos[1], size[0], size[1])
        else:
            print(
                "[WARNING] [EventableWidget.add_uneventable_zone] The zone exceeds the widget"
            )

    def remove_uneventable_zone(self, pos, size):
        """
        Remove an uneventable zone.

        :type pos: tuple
        :param pos: A (x, y) tuple representing the top left corner of the
            uneventable zone (in pixel).

        :type size: tuple
        :param size: A (w, h) tuple representing the size in pixel of the
            uneventable zone.
        """

        if (pos[0], pos[1], size[0], size[1]) in self.uneventable_zones:
            self.uneventable_zones.remove((pos[0], pos[1], size[0], size[1]))

    def is_in_uneventable_zone(self, pos):
        """
        Check if a position is within an eventable zone.

        :type pos: tuple
        :param pos: A (x, y) tuple representing the position to check.

        :rtype: bool
        :returns: True if the position is within an uneventable zone.
        """

        for zone in self.uneventable_zones:
            if (
                pos[0] >= zone[0]
                and pos[0] <= zone[0] + zone[2]
                and pos[1] >= zone[1]
                and pos[1] <= zone[1] + zone[3]
            ):
                return True
        return False
