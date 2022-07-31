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
Provide a MenuWidget base class.

Created on 08/10/2018.
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH
from gui.image_transformer import stretch_image
from gui.widget import Widget


class MenuWidget(Widget):
    """
    Create a widget used to pack sub_widgets which will be updated by this
            menu.
    """

    DEFAULT_KWARGS = {"background_image": os.path.join(GUI_IMAGE_PATH, "frame.png")}

    def __init__(self, activity, pos, **kwargs):
        """
        Initialize a new Menu objects.

        :type activity: gui.activity.Activity
        :param activity: The parent activity of this widget.

        :type pos: tuple
        :param pos: The default position of the widget in a (x, y) tuple where
                x and y are integers.

        background_image can be defined.
        """

        MenuWidget.update_default_kwargs(kwargs)
        Widget.__init__(self, activity, pos, **kwargs)

        self.sub_widgets = {}
        self.background_image = None
        self.activity.disable_widgets()
        self.load_background_image()
        self.init_widgets()

    def load_background_image(self):
        """
        Create the background from an image stretched to the widget size.
        """

        if self.kwargs["background_image"]:
            self.background_image = stretch_image(
                self.activity.window.get_image(self.kwargs["background_image"]),
                self.kwargs["size"],
                5,
            )

    def init_widgets(self):
        """
        Initialize all sub_widgets.
        """

    def add_sub_widget(
        self, widget_name, widget_type, pos, *widgetArgs, **widgetKwargs
    ):
        """
        Create and add a new widget to this menu.

        :type widget_name: str
        :param widget_name: A string to identify the subwidget.

        :type widget_type: type
        :param widget_type: A type used to create the subwidget.

        :type pos: tuple
        :param pos: The default position of the subwidget relative to the
                upper left corner of the menu.

        Arguments and keyword arguments to pass to the subwidget can be
                defined then.
        """

        if widget_name in self.sub_widgets:
            print(
                "[WARNING] [MenuWidget.add_sub_widget] A widget "
                + f'called "{widget_name}" already exists in'
                + " this MenuWidget ! Destroying it"
            )

            if not self.sub_widgets[widget_name].is_destroyed:
                self.sub_widgets[widget_name].destroy()

        real_pos = self.get_real_pos()
        self.sub_widgets[widget_name] = widget_type(
            self.activity,
            (pos[0] + real_pos[0], pos[1] + real_pos[1]),
            *widgetArgs,
            **widgetKwargs,
        )

    def remove_sub_widget(self, widget_name):
        """
        Remove a subwidget from this menu.

        :type widget_name: str
        :param widget_name: The name used to identify the subwidget.
        """

        if widget_name in self.sub_widgets:
            if not self.sub_widgets[widget_name].is_destroyed:
                self.sub_widgets[widget_name].destroy()
            self.sub_widgets.pop(widget_name)
        else:
            print(
                "[WARNING] [MenuWidget.remove_sub_widget] No widget called"
                + f' "{widget_name}" in this MenuWidget'
            )

    def config_sub_widget(self, widget_name, **kwargs):
        """
        Call config method on a given subwidget.

        :type widget_name: str
        :param widget_name: The name used to identify the subwidget.

        Keyword arguments are passed to the subwidget.config method.
        """

        if widget_name in self.sub_widgets:
            self.sub_widgets[widget_name].config(**kwargs)
        else:
            print(
                "[WARNING] [MenuWidget.config_sub_widget] No widget called"
                + f' "{widget_name}" in this MenuWidget'
            )

    def update(self, delta_time):
        """
        Update the menu and its sub_widgets.

        :type delta_time: float
        :param delta_time: Time elapsed since the last call of this method (in
                seconds).
        """

        if self.background_image:
            self.activity.window.draw_image(self.background_image, self.get_real_pos())

        for widget in tuple(self.sub_widgets.values()):
            if not widget.is_destroyed:
                widget.update(delta_time)

    def on_event(self, event):
        """
        This method is called on all user events detected by Pygame.

        :type event: pygame.event.Event
        :param event: The event to handle.
        """

        for widget in tuple(self.sub_widgets.values()):
            if not widget.is_destroyed:
                widget.on_event(event)

    def destroy(self):
        """
        Destroy the menu and its sub_widgets.
        """

        for widget in tuple(self.sub_widgets.values()):
            if not widget.is_destroyed:
                widget.destroy()
        self.sub_widgets.clear()
        self.activity.enable_widgets()
        Widget.destroy(self)

    def config(self, **kwargs):
        """
        Change some kwargs of the menu.
        """

        Widget.config(self, **kwargs)
        if "enable" in kwargs:
            for widget in self.sub_widgets.values():
                widget.config(enable=kwargs["enable"])
