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
Provide a menu to display when the game is paused.

Created on 18/08/2018
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH

from gui.clickable_text import ClickableText
from gui.menu_widget import MenuWidget
from gui.option_menu import OptionMenu
from gui.text import Text


class PauseMenu(MenuWidget):
    """
    A menu to display when the game is paused.
    """

    DEFAULT_KWARGS = {"font_size": 20, "font": os.path.join(GUI_IMAGE_PATH, "font.ttf")}

    def __init__(self, activity, pos, resume_fct, quit_fct, **kwargs):
        """
        Initialize a new Pause_menu object.

        :type activity: gui.activity.Activity
        :param activity: The parent activity of this widget.

        :type pos: tuple
        :param pos: The position of the widget in a (x, y) tuple where x and y
            are integers.

        :type resume_fct: callable
        :param resume_fct: A function, class or method which can be called on click
            on the "resume" button.

        :type quit_fct: callable
        :param quit_fct: A function, class or method which can be called on click
            on the "quit" button.
        """

        PauseMenu.update_default_kwargs(kwargs)
        MenuWidget.__init__(self, activity, pos, **kwargs)

        self.resume_fct = resume_fct
        self.quit_fct = quit_fct

    def init_widgets(self):
        """
        Create widgets displayed in this dialog.
        """

        width, height = self.kwargs["size"]
        font = self.kwargs["font"]
        font_size = self.kwargs["font_size"]
        medium_font_size = font_size - 3

        pos_x = int(width * 0.5)
        pos_y = int(height * 0.2)
        self.add_sub_widget(
            "titleText",
            Text,
            (pos_x, pos_y),
            "Pause",
            anchor=(0, 0),
            font=font,
            font_size=font_size,
        )

        pos_y = int(height * 0.4)
        self.add_sub_widget(
            "resumeClickableText",
            ClickableText,
            (pos_x, pos_y),
            "continuer",
            anchor=(0, 0),
            font=font,
            font_size=medium_font_size,
            on_click_fct=self.destroy,
        )

        pos_y = int(height * 0.6)
        self.add_sub_widget(
            "optionClickableText",
            ClickableText,
            (pos_x, pos_y),
            "options",
            anchor=(0, 0),
            font=font,
            font_size=medium_font_size,
            on_click_fct=self.open_option_menu,
        )

        pos_y = int(height * 0.8)
        self.add_sub_widget(
            "quitClickableText",
            ClickableText,
            (pos_x, pos_y),
            "quitter",
            anchor=(0, 0),
            font=font,
            font_size=medium_font_size,
            on_click_fct=self.leave_level,
        )

    def destroy(self):
        """
        Destroy the widget and its subwidgets, then call resume_fct.
        """

        MenuWidget.destroy(self)
        self.resume_fct()

    def leave_level(self):
        """
        Destroy the widget and its subwidgets, then call quit_fct.
        """

        MenuWidget.destroy(self)
        self.quit_fct()

    def open_option_menu(self):
        """
        Create an Option_menu.
        """

        layout = self.activity.layout
        pos_x, pos_y = layout.get_widget_pos("option_menu")
        size = layout.get_widget_size("option_menu")
        anchor = layout.get_widget_anchor("option_menu")
        fsize = layout.get_font_size("option_menu")

        realpos_x, realpos_y = self.get_real_pos()
        pos_x, pos_y = pos_x - realpos_x, pos_y - realpos_y
        self.add_sub_widget(
            "option_menu",
            OptionMenu,
            (pos_x, pos_y),
            self.on_option_menu_destroy,
            size=size,
            anchor=anchor,
            font_size=fsize,
        )

    def on_option_menu_destroy(self):
        """
        This method is called when the Option_menu is destroyed.
        """

        self.remove_sub_widget("option_menu")
        self.activity.disable_widgets()
        self.config(enable=True)
