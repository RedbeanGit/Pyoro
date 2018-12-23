# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 18/08/2018
	@version: 1.1
=========================
"""

import os

from game.config import GUI_IMAGE_PATH, WIDTH, HEIGHT
from gui.clickable_text import Clickable_text
from gui.menu_widget import Menu_widget
from gui.option_menu import Option_menu
from gui.text import Text

class Pause_menu(Menu_widget):

	DEFAULT_KWARGS = {
		"size": [WIDTH // 2.5, HEIGHT // 2],
		"fontSize": 20,
		"font": os.path.join(GUI_IMAGE_PATH, "font.ttf")
	}

	def __init__(self, activity, pos, resumeFct, quitFct, **kwargs):
		Pause_menu.updateDefaultKwargs(kwargs)
		Menu_widget.__init__(self, activity, pos, **kwargs)

		self.resumeFct = resumeFct
		self.quitFct = quitFct

	def initWidgets(self):
		realPos = self.getRealPos()
		w, h = self.kwargs["size"]
		f = self.kwargs["font"]
		fs = self.kwargs["fontSize"]
		
		px = int(w * 0.5)
		py = int(h * 0.2)
		self.addSubWidget("titleText", Text, (px, py), "Pause", anchor = (0, 0), font = f, fontSize = fs + 15)
		py = int(h * 0.4)
		self.addSubWidget("resumeClickableText", Clickable_text, (px, py), "continuer", anchor = (0, 0), font = f, fontSize = fs, onClickFct = self.destroy)
		py = int(h * 0.6)
		self.addSubWidget("optionClickableText", Clickable_text, (px, py), "options", anchor = (0, 0), font = f, fontSize = fs, onClickFct = self.openOptionMenu)
		py = int(h * 0.8)
		self.addSubWidget("quitClickableText", Clickable_text, (px, py), "quitter", anchor = (0, 0), font = f, fontSize = fs, onClickFct = self.leaveLevel)

	def destroy(self):
		Menu_widget.destroy(self)
		self.resumeFct()

	def leaveLevel(self):
		Menu_widget.destroy(self)
		self.quitFct()

	def openOptionMenu(self):
		w, h = self.kwargs["size"]
		self.addSubWidget("optionMenu", Option_menu, (w // 2, h // 2), self.onOptionMenuDestroy, anchor = (0, 0))

	def onOptionMenuDestroy(self):
		self.removeSubWidget("optionMenu")
		self.activity.disableWidgets()
		self.config(enable = True)