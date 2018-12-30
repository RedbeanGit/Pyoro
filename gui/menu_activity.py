# -*- coding: utf-8 -*-

"""
Provide an activity to manage the main menu.

Created on 10/04/2018
"""

from game.config import GUI_IMAGE_PATH
from game.level import Level
from game.util import Game

from gui.activity import Activity
from gui.button import Button
from gui.image_transformer import Image_transformer
from gui.layout import Layout
from gui.level_drawer import Level_drawer
from gui.play_button import Play_button
from gui.option_menu import Option_menu

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import os


class Menu_activity(Activity):
	""" Layout managing the menu's components """

	def __init__(self, window, gameId):
		self.window = window
		self.level = Level(self, gameId, botMode = True)
		self.levelDrawer = Level_drawer(self.level, self.window)
		self.titlePos = [0, 0]
		self.level.init()
		Activity.__init__(self, window)

	def initImages(self):
		w, h = self.layout.getWidgetSize("title")
		x, y = self.layout.getWidgetPos("title")
		ax, ay = self.layout.getWidgetAnchor("title")
		self.titlePos = [x - w * (ax + 1) / 2, y - h * (ay + 1) / 2]

		self.images["title"] = Image_transformer.resize(self.window.getImage(
			os.path.join(GUI_IMAGE_PATH, "title.png")), (w, h))

		self.levelDrawer.initImages()
		Activity.initImages(self)

	def initSounds(self):
		self.__initSounds__(("intro",), os.path.join("data", "audio", "musics"), "music")
		self.sounds["intro"].play()
		Game.audioPlayer.setSpeed(1)

	def initWidgets(self):
		widgetInfos = {
			"play_button_1": {
				"type": Play_button,
				"args": (0,),
				"kwargs": {
					"onClickFct": self.window.setGameRender
				}
			},
			"play_button_2": {
				"type": Play_button,
				"args": (1,),
				"kwargs": {
					"onClickFct": self.window.setGameRender,
					"enable": self.isPyoro2Unlocked()
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
				fontSize = fsize,
				**kwargs["kwargs"]
			)

	def createOptionMenu(self):
		size = self.layout.getWidgetSize("option_menu")
		pos = self.layout.getWidgetPos("option_menu")
		anchor = self.layout.getWidgetAnchor("option_menu")

		self.addWidget("option_menu", Option_menu, pos, \
			self.onOptionMenuDestroy, size = size, anchor = anchor)

	def onOptionMenuDestroy(self):
		self.widgets["play_button_2"].config(enable = self.isPyoro2Unlocked())
		self.removeWidget("option_menu")

	def update(self, deltaTime):
		self.level.update(deltaTime)
		self.levelDrawer.update(deltaTime)
		self.window.drawImage(self.images["title"], self.titlePos)
		Activity.update(self, deltaTime)

	def isPyoro2Unlocked(self):
		highScore = self.window.getOption("high score")
		return highScore[0] >= 10000
