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
Provide a class to load, update and manage mods

Created on 18/11/2018
"""

import os
import sys

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.util import get_external_data_path


class Mod:
    """
    Load, update and manage a mod.
    """

    modList = []

    def __init__(self, name):
        """
        Initialize a Mod object.

        :type name: str
        :param name: The name of the mod.
        """

        self.name = name
        self.module = None
        self.loaded = False
        Mod.add_folder_to_path()

    def load(self):
        """
        Load a mod by importing it.

        :rtype: bool
        :returns: True if it's a success, otherwise False.
        """

        try:
            exec("import " + self.name)
            exec("self.module = " + self.name)
            self.loaded = True
            return True
        except ImportError:
            print(f'[WARNING] [Mod.load] Unable to import "{self.name}"')
        return False

    def init(self, window):
        """
        Initialize a mod by passing to it the current gui.window.Window.

        :type window: gui.window.Window
        :param window: The current game window.

        :rtype: bool
        :returns: True if it's a success, otherwise False.
        """

        if "init" in dir(self.module):
            if callable(self.module.init):
                try:
                    self.module.init(window)
                    return True
                except Exception:
                    print(
                        "[WARNING] [Mod.init] Something wrong happened "
                        + f'while initializing "{self.name}"'
                    )
        return False

    def update(self, window, delta_time):
        """
        Update a mod by passing to it the current gui.window.Window
        and the elapsed time since the last update.

        :type window: gui.window.Window
        :param window: The current game window.

        :type delta_time: float
        :param delta_time: Elapsed time since the last update.

        :rtype: bool
        :returns: True if it's a success, otherwise False.
        """

        if "update" in dir(self.module):
            if callable(self.module.update):
                try:
                    self.module.update(window, delta_time)
                    return True
                except Exception:
                    print(
                        "[WARNING] [Mod.update] Something wrong happened"
                        + f' while updating "{self.name}"'
                    )
        return False

    @classmethod
    def load_mods(cls):
        """
        Load all mods in the mod folder.
        """

        mod_folder = os.path.join(get_external_data_path(), "mods")

        if not os.path.exists(mod_folder):
            os.makedirs(mod_folder)

        file_names = os.listdir(mod_folder)

        for file_name in file_names:
            mod_name, ext = os.path.splitext(file_name)
            if mod_name != "__init__" and ext in (".py", ".pyc", ".pyd", ".pyw"):
                mod = Mod(mod_name)
                cls.modList.append(mod)
                mod.load()

    @classmethod
    def init_mods(cls, window):
        """
        Initialize all loaded mods.
        """

        for mod in cls.modList:
            if mod.loaded:
                mod.init(window)

    @classmethod
    def update_mods(cls, window, delta_time):
        """
        Update all loaded mods.
        """

        for mod in cls.modList:
            if mod.loaded:
                mod.update(window, delta_time)

    @staticmethod
    def add_folder_to_path():
        """
        Add the mod folder to path.
        """

        mod_folder = os.path.join(get_external_data_path(), "mods")
        if mod_folder not in sys.path:
            sys.path.append(mod_folder)
