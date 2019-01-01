# -*- coding: utf-8 -*-

"""
Provide an activity to manage the main menu.

Created on 10/04/2018
"""

from game.config import GUI_IMAGE_PATH
from game.util import Game

from gui.activity import Activity
from gui.button import Button
from gui.image_widget import Image_widget
from gui.level_drawer import Level_drawer
from gui.play_button import Play_button
from gui.option_menu import Option_menu

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import os


class Menu_activity(Activity):
	"""
	Layout managing the menu's components
	"""

	def __init__(self, window, gameId):
		"""
		Initialize a new Menu_activity object.

		:type window: gui.window.Window
		:param window: The parent game window.

		:type gameId: int
		:param gameId: The gameId of the level in background.
			0 = Pyoro, 1 = Pyoro 2.
		"""

		Activity.__init__(self, window)
		self.levelDrawer = Level_drawer(self, gameId, botMode = True)

	def initSounds(self):
		"""
		Reference the "intro.wav" music and start to play it.
		This method reset the global Audio_player speed.
		"""

		self.__initSounds__(("intro",), os.path.join("data", "audio", "musics"), "music")
		Game.audioPlayer.setSpeed(1)
		self.sounds["intro"].play(-1)

	def initWidgets(self):
		"""
		Create widgets (Play, option and quit buttons).
		"""

		widgetInfos = {
			"title_image": {
				"type": Image_widget,
				"args": (os.path.join(GUI_IMAGE_PATH, "title.png"),),
				"kwargs": {}
			},
			"play_button_1": {
				"type": Play_button,
				"args": (0,),
				"kwargs": {
					"onClickFct": self.window.setGameRender,
					"textAnchor": (0, -0.1)
				}
			},
			"play_button_2": {
				"type": Play_button,
				"args": (1,),
				"kwargs": {
					"onClickFct": self.window.setGameRender,
					"enable": self.isPyoro2Unlocked(),
					"textAnchor": (0, -0.1)
				}
			},
			"option_button": {
				"type": Button,
				"args": (),
				"kwargs": {
					"text": "Options",
					"onClickFct": self.createOptionMenu
				}
			},
			"quit_button": {
				"type": Button,
				"args": (),
				"kwargs": {
					"text": "Quitter",
					"onClickFct": self.window.destroy
				}
			}
		}

		for widgetName, kwargs in widgetInfos.items():
			pos = self.layout.getWidgetPos(widgetName)
			size = self.layout.getWidgetSize(widgetName)
			anchor = self.layout.getWidgetAnchor(widgetName)
			fsize = self.layout.getFontSize(widgetName)

			self.addWidget(
				widgetName,
				kwargs["type"],
				pos,
				*kwargs["args"],
				size = size,
				anchor = anchor,
				textKwargs = {"fontSize": fsize},
				**kwargs["kwargs"]
			)

	def createOptionMenu(self):
		"""
		Display an option menu.
		"""

		size = self.layout.getWidgetSize("option_menu")
		pos = self.layout.getWidgetPos("option_menu")
		anchor = self.layout.getWidgetAnchor("option_menu")

		self.addWidget("option_menu", Option_menu, pos, \
			self.onOptionMenuDestroy, size = size, anchor = anchor)

	def onOptionMenuDestroy(self):
		"""
		This method is called when the option menu is destroyed.
		Remove the option menu from the updatable widgets list.
		"""

		self.widgets["play_button_2"].config(enable = self.isPyoro2Unlocked())
		self.removeWidget("option_menu")

	def update(self, deltaTime):
		"""
		Update the level and redraw graphical components.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last call of this method
			(in seconds).
		"""

		self.levelDrawer.update(deltaTime)
		Activity.update(self, deltaTime)

	def isPyoro2Unlocked(self):
		"""
		Check if Pyoro 2 is unlocked. To unlock Pyoro 2, the score must be
			greater than 10000.

		:rtype: bool
		:returns: True if Pyoro 2 is unlocked, otherwise False.
		"""

		highScore = Game.options.get("high score", [0, 0])
		return highScore[0] >= 10000
