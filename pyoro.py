# -*- coding: utf-8 -*-

"""
Main module for Pyoro to start from lem launcher.

Created on 16/01/2019
"""

from pyoro_core.util import loadOptions, saveOptions
from pyoro_core.constants import VERSION, Game
from pyoro_core.activity import Splash_activity, Menu_activity, Level_activity
from pyoro_core.view import Splash_view, Menu_view, Level_view

__author__ = "Julien Dubois"
__version__ = "2.0.0"

import os

from lemapi.api import start_activity, stop_activity, get_app_path


def main(appId):
	print("[Pyoro] [INFO] [main] Starting pyoro v" + VERSION)
	os.chdir(get_app_path())
	Game.ID = appId
	loadOptions()
	create_splash()


def exit():
	print("[INFO] [exit] Stopping Pyoro v" + VERSION)
	saveOptions()


def create_splash():
	view = Splash_view()
	activity = Splash_activity(view, create_menu)
	start_activity(activity)
	activity.boot()


def create_menu(gameId = 0):
	stop_activity()
	view = Menu_view()
	activity = Menu_activity(view, create_level, gameId)
	start_activity(activity)


def create_level(gameId = 0):
	view = Level_view()
	activity = Level_activity(view, stop_activity, gameId)
	start_activity(activity)
