# -*- coding: utf-8 -*-

"""
Main module for Pyoro to start from lem launcher.

Created on 16/01/2019
"""

from audio.audio_player import Audio_player
from game.util import Game, loadOptions, saveOptions
from game.config import VERSION
from game.activity import Splash_activity, Menu_activity, Level_activity
from graphism.view import Splash_view, Menu_view, Level_view

__author__ = "Julien Dubois"
__version__ = "2.0.0"

from lemapi.api import start_activity


def main(appId):
	print("[INFO] [main] Starting pyoro v" + VERSION)
	Game.appId = appId
	Game.options = loadOptions()
	Game.audioPlayer = Audio_player()
	create_splash()


def exit():
	print("[INFO] [exit] Stopping Pyoro v" + VERSION)
	if Game.audioPlayer:
		Game.audioPlayer.stop()
	if Game.options:
		saveOptions(Game.options)


def create_splash():
	view = Splash_view()
	activity = Splash_activity(view, create_menu)
	start_activity(activity)
	activity.boot()


def create_menu(gameId = 0):
	view = Menu_view()
	activity = Menu_activity(view, create_level, gameId)
	start_activity(activity)


def create_level(gameId = 0):
	view = Level_view()
	activity = Level_activity(view, create_menu, gameId)
	start_activity(activity)
