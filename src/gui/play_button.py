# -*- coding:utf-8 -*-

#	This file is part of Pyoro (A Python fan game).
#
#	Metawars is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Metawars is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
Provide a Play_button class.

Created on 18/08/2018.
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH
from game.util import Game
from gui.button import Button


class Play_button(Button):
	"""
	Create a button displayed in the main menu to start a new game.
	"""

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
		"""
		Initialize a new Play_button object.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The default position of the button in a (x, y) tuple where
			x and y are integers.

		:type gameId: int
		:param gameId: The game to launch when clicked (0=Pyoro, 1=Pyoro 2).

		backgroundImage, onHoverBackgroundImage, onClickBackgroundImage,
		onMiddleClickBackgroundImage, onRightClickBackgroundImage and 
		disableBackgroundImage can be defined.
		"""

		Play_button.updateDefaultKwargs(kwargs)
		self.gameId = gameId
		Button.__init__(self, activity, pos, **kwargs)
		if self.kwargs["enable"]:
			self.config(text = "High Score:{}".format(Game.options.get( \
				"high score", [0, 0])[gameId]))

	def loadBackgroundImages(self):
		"""
		Load backgrounds by stretching the images associated to the give
			gameId.
		"""

		backNames = ("backgroundImage", "onHoverBackgroundImage", \
			"onClickBackgroundImage", "onMiddleClickBackgroundImage", \
			"onRightClickBackgroundImage", "disableBackgroundImage")
		for backName in backNames:
			if self.kwargs[backName]:
				if "{}" in self.kwargs[backName]:
					self.kwargs[backName] = self.kwargs[backName] \
						.format(self.gameId + 1)
		Button.loadBackgroundImages(self)

	def onEndClick(self):
		"""
		Launch the game.
		"""

		if self.clicked:
			self.clicked = False
			if self.kwargs["onClickFct"]:
				self.kwargs["onClickFct"](self.gameId, \
					*self.kwargs["onClickArgs"], \
					**self.kwargs["onClickKwargs"])
