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
Provide a base class for activities.

Created on 15/08/2018
"""

import collections
import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.util import Game
from gui.layout import Layout


class Activity:
    """
    Abstract class for all activities.
    """

    def __init__(self, window):
        """
        Initialize a new Activity object.

        :type window: gui.window.Window
        :param window: The parent window which will manage this activity.
        """

        self.window = window
        self.layout = Layout(window)
        self.widgets = collections.OrderedDict()
        self.sounds = {}

        self.layout.load()
        self.init_sounds()
        self.init_widgets()

    def __init_sounds__(self, sound_names, folder, audio_type="sound"):
        """
        Useful method to easily load sounds or musics which will be used later
        by this activity. Do not override this method.

        :type sound_names: tuple
        :param sound_names: Base filename of the sounds to load.

        :type folder: str
        :param folder: The filepath of the folder where sounds are located.

        :type audio_type: str
        :param audio_type: (Optional) How to load the sound (as sound or as music).
            Default is "sound". It can be "sound" or "music".
        """

        if audio_type == "sound":
            fct = Game.audio_player.get_sound
        elif audio_type == "music":
            fct = Game.audio_player.get_music
        for name in sound_names:
            self.sounds[name] = fct(os.path.join(folder, f"{name}.wav"))

    def init_sounds(self):
        """
        This method should be override. It's called when the activity is
        initialized. It's used to load the sounds used by this activity.
        """

    def init_widgets(self):
        """
        This method should be override. It's called when the activity is
        initialized. It's used to load the widgets used by this activity.
        """

    def add_widget(self, widget_name, widget_type, *args, **kwargs):
        """
        Add a widget with a defined name and arguments.

        :type widget_name: str
        :param widget_name: The name of the widget. This name can be use later to
            get or remove the widget.

        :type widget_type: class
        :param widget_type: The class of the widget to add. This class is used to
            create the widget.
        """

        if widget_name in self.widgets:
            print(
                f"[WARNING] [Layout.add_widget] Widget '{widget_name}' already exists"
            )
        else:
            widget = widget_type(self, *args, **kwargs)
            self.widgets[widget_name] = widget

    def remove_widget(self, widget_name):
        """
        Remove a widget from this activity.

        :type widget_name: str
        :param widget_name: The name of the widget to destroy and remove.
        """

        if widget_name in self.widgets:
            if not self.widgets[widget_name].is_destroyed:
                self.widgets[widget_name].destroy()
            self.widgets.pop(widget_name)
        else:
            print(
                f"[WARNING] [Layout.remove_widget] '{widget_name}' not in widget list"
            )

    def enable_widgets(self):
        """
        Enable all widgets of this activity.
        """

        for widget in tuple(self.widgets.values()):
            widget.config(enable=True)

    def disable_widgets(self):
        """
        Disable all widgets of this activity.
        """

        for widget in tuple(self.widgets.values()):
            widget.config(enable=False)

    def update_event(self, event):
        """
        Update all widgets of this activity by giving to them a defined pygame
        event.

        :type event: pygame.event.Event
        :param event: The event to pass to the widgets.
        """

        for widget in tuple(self.widgets.values()):
            if not widget.is_destroyed:
                widget.on_event(event)

    def update(self, delta_time):
        """
        Update all graphical components of this activity.

        :type delta_time: float
        :param delta_time: Time elapsed since the last call of this method (in
            seconds).
        """

        for widget in tuple(self.widgets.values()):
            if not widget.is_destroyed:
                widget.update(delta_time)

    def destroy(self):
        """
        Destroy all widgets of this activity.
        """

        for widget in tuple(self.widgets.values()):
            if not widget.is_destroyed:
                widget.destroy()
        self.widgets.clear()
