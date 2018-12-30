# -*- coding:utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 30/10/2018
	@version: 1.1
=========================
"""

import os

from game.config import GUI_IMAGE_PATH
from gui.menu_widget import Menu_widget
from gui.clickable_text import Clickable_text
from gui.text import Text

class Dialog_menu(Menu_widget):

	DEFAULT_KWARGS = {
		"font": os.path.join(GUI_IMAGE_PATH, "font.ttf"),
		"positiveArgs": (),
		"positiveKwargs": {},
		"negativeFct": None,
		"negativeArgs": (),
		"negativeKwargs": {},
		"description": ""
	}

	def __init__(self, activity, pos, message, positiveFct, **kwargs):
		Dialog_menu.updateDefaultKwargs(kwargs)

		self.message = message
		self.positiveFct = positiveFct

		Menu_widget.__init__(self, activity, pos, **kwargs)

	def initWidgets(self):
		w, h = self.kwargs["size"]
		f = self.kwargs["font"]
		px = int(w * 0.5)
		py = int(h * 0.25)
		self.addSubWidget("titleText", Text, (px, py), self.message, font = f, fontSize = 22, anchor = (0, 0))

		if self.kwargs["description"]:
			px = int(w * 0.1)
			py = int(h * 0.4)
			self.addSubWidget("descText", Text, (px, py), self.kwargs["description"], font = f, fontSize = 18, anchor = (-1, 0))

		py = int(h * 0.8)
		px = int(w * 0.75)
		if self.kwargs["negativeFct"]:
			self.addSubWidget("positiveText", Clickable_text, (px, py), "oui", font = f, fontSize = 18, anchor = (0, 0), onClickFct = self.positiveAction)
			px = int(w * 0.25)
			self.addSubWidget("negativeText", Clickable_text, (px, py), "non", font = f, fontSize = 18, anchor = (0, 0), onClickFct = self.negativeAction)
		else:
			self.addSubWidget("positiveText", Clickable_text, (px, py), "ok", font = f, fontSize = 18, anchor = (0, 0), onClickFct = self.positiveAction)

	def negativeAction(self):
		self.destroy()
		self.kwargs["negativeFct"](*self.kwargs["negativeArgs"], **self.kwargs["negativeKwargs"])

	def positiveAction(self):
		self.destroy()
		self.positiveFct(*self.kwargs["positiveArgs"], **self.kwargs["positiveKwargs"])
