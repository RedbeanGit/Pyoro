# -*- coding: utf-8 -*-

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
Provide a widget to create a "Game over" menu.

Created on 21/08/2018
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH
from gui.clickable_text import Clickable_text
from gui.menu_widget import Menu_widget
from gui.text import Text


class Game_over_menu(Menu_widget):
	"""
	This class create a "Game over" menu widget displayed when Pyoro dies
	"""

	DEFAULT_KWARGS = {
		"fontSize": 20,
		"font": os.path.join(GUI_IMAGE_PATH, "font.ttf")
	}

	def __init__(self, activity, pos, score, quitFct, **kwargs):
		"""
		Initialise a new Game_over_menu object.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The default position of the menu in a (x, y) tuple where
			x and y are integers.

		:type score: int
		:param score: The score at the of the game.

		:type quitFct: callable
		:param quitFct: A callable to run when the player click on the "Quit"
			button.
		"""

		Game_over_menu.updateDefaultKwargs(kwargs)

		self.quitFct = quitFct
		self.score = score

		Menu_widget.__init__(self, activity, pos, **kwargs)

	def initWidgets(self):
		"""
		Create subwidgets which will compose the menu.
		"""

		realPos = self.getRealPos()
		w, h = self.kwargs["size"]
		f = self.kwargs["font"]
		ts = self.kwargs["fontSize"]; ms = ts - 3

		px = int(w * 0.5)
		py = int(h * 0.25)
		self.addSubWidget("titleText", Text, (px, py), "Game Over", \
			anchor = (0, 0), font = f, fontSize = ts)
		py = int(h * 0.50)
		self.addSubWidget("scoreText", Text, (px, py), \
			"score : {}".format(self.score), anchor = (0, 0), font = f, \
			fontSize = ms)
		py = int(h * 0.75)
		self.addSubWidget("quitClickableText", Clickable_text, (px, py), \
			"quitter", anchor = (0, 0), font = f, fontSize = ms, \
			onClickFct = self.destroy)

	def destroy(self):
		"""
		Destroy the widget and call self.quitFct.
		"""
		
		Menu_widget.destroy(self)
		self.quitFct()
