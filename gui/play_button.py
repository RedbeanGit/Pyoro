# -*- coding:utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 18/08/2018
	@version: 1.1
=========================
"""

import os

from game.config import GUI_IMAGE_PATH
from game.util import Game
from gui.button import Button

class Play_button(Button):

	DEFAULT_KWARGS = {
		"backgroundAnchor": (0, -0.05),

		"backgroundImage": os.path.join(GUI_IMAGE_PATH, "play button {}", "play_button.png"),
		"onHoverBackgroundImage": os.path.join(GUI_IMAGE_PATH, "play button {}", "play_button_hover.png"),
		"onClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "play button {}", "play_button_click.png"),
		"onMiddleClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "play button {}", "play_button_middle_click.png"),
		"onRightClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "play button {}", "play_button_right_click.png"),
		"disableBackgroundImage": os.path.join(GUI_IMAGE_PATH, "play button {}", "play_button_disable.png")
	}

	def __init__(self, activity, pos, gameId, **kwargs):
		Play_button.updateDefaultKwargs(kwargs)
		self.gameId = gameId
		Button.__init__(self, activity, pos, **kwargs)
		if self.kwargs["enable"]:
			self.config(text = "High Score:{}".format(Game.options.get("high score", [0, 0])[gameId]))

	def loadBackgroundImages(self):
		backNames = ("backgroundImage", "onHoverBackgroundImage", "onClickBackgroundImage", "onMiddleClickBackgroundImage", "onRightClickBackgroundImage", "disableBackgroundImage")
		for backName in backNames:
			if self.kwargs[backName]:
				if "{}" in self.kwargs[backName]:
					self.kwargs[backName] = self.kwargs[backName].format(self.gameId + 1)
		Button.loadBackgroundImages(self)

	def onEndClick(self):
		if self.clicked:
			self.clicked = False
			if self.kwargs["onClickFct"]:
				self.kwargs["onClickFct"](self.gameId, *self.kwargs["onClickArgs"], **self.kwargs["onClickKwargs"])
