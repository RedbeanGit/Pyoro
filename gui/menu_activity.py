# -*- coding: utf-8 -*-

"""
Provide an activity to manage the main menu.

Created on 10/04/2018
"""

from game.config import GUI_IMAGE_PATH, WIDTH, HEIGHT
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
		ww, wh = self.window.getSize()
		ts = int((ww + wh) * 0.015625) 
		widgetInfos = {
			"playButton1": {
				"type": Play_button,
				"args": (0,),
				"kwargs": {
					"fontSize": ts,
					"onClickFct": self.window.setGameRender
				}
			},
			"playButton2": {
				"type": Play_button,
				"args": (1,),
				"kwargs": {
					"fontSize": ts,
					"onClickFct": self.window.setGameRender, 
					"enable": self.isPyoro2Unlocked()
				}
			},
			"optionButton": {
				"type": Button,
				"args": (),
				"kwargs": {
					"fontSize": ts,
					"text": "Options",
					"onClickFct": self.createOptionMenu
				}
			},
			"quitButton": {
				"type": Button,
				"args": (),
				"kwargs": {
					"fontSize": ts,
					"text": "Quitter",
					"onClickFct": self.window.destroy
				}
			}
		}

		for widgetName, kwargs in widgetInfos.items():
			x, y = self.layout.getWidgetPos(widgetName)
			w, h = self.layout.getWidgetSize(widgetName)
			ax, ay = self.layout.getWidgetAnchor(widgetName)
			self.addWidget(
				widgetName, 
				kwargs["type"], 
				(x, y),
				*kwargs["args"],
				size = (w, h),
				anchor = (ax, ay),
				**kwargs["kwargs"]
			)
	
	def createOptionMenu(self):
		ww, wh = self.window.getSize()
		self.addWidget("optionMenu", Option_menu, (ww // 2, wh // 2), self.onOptionMenuDestroy, anchor = (0, 0))

	def onOptionMenuDestroy(self):
		self.widgets["playButton2"].config(enable = self.isPyoro2Unlocked())
		self.removeWidget("optionMenu")

	def update(self, deltaTime):
		ww, wh = self.window.getSize()

		self.level.update(deltaTime)
		self.levelDrawer.update(deltaTime)
		self.window.drawImage(self.images["title"], self.titlePos)
		Activity.update(self, deltaTime)

	def isPyoro2Unlocked(self):
		highScore = self.window.getOption("high score")
		return highScore[0] >= 10000