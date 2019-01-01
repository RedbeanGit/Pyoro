# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 21/08/2018
	@version: 1.1
=========================
"""

import os

from game.config import GUI_IMAGE_PATH
from gui.clickable_text import Clickable_text
from gui.menu_widget import Menu_widget
from gui.text import Text

class Game_over_menu(Menu_widget):

	DEFAULT_KWARGS = {
		"fontSize": 20,
		"font": os.path.join(GUI_IMAGE_PATH, "font.ttf")
	}

	def __init__(self, activity, pos, score, quitFct, **kwargs):
		Game_over_menu.updateDefaultKwargs(kwargs)

		self.quitFct = quitFct
		self.score = score

		Menu_widget.__init__(self, activity, pos, **kwargs)

	def initWidgets(self):
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
		Menu_widget.destroy(self)
		self.quitFct()
