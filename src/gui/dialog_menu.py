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
Provide a Dialog_menu class.

Created on 30/10/2018.
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH
from gui.menu_widget import Menu_widget
from gui.clickable_text import Clickable_text
from gui.text import Text


class Dialog_menu(Menu_widget):
	"""
	Create a menu to alert the player or to ask his opinion.
	"""

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
		"""
		Initialize a new Dialog_menu objects.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The default position of the widget in a (x, y) tuple where
			x and y are integers.

		:type message: str
		:param message: A message to display to the player.

		:type positiveFct: callable
		:param positiveFct: A callable to call on click on the first button.

		font, positiveArgs, positiveKwargs, negativeFct, negativeArgs,
		negativeKwargs and description can be defined.

		If negativeFct is defined, a second button is created.
		"""

		Dialog_menu.updateDefaultKwargs(kwargs)

		self.message = message
		self.positiveFct = positiveFct

		Menu_widget.__init__(self, activity, pos, **kwargs)

	def initWidgets(self):
		"""
		Create and initialize all subwidgets.
		"""

		w, h = self.kwargs["size"]
		f = self.kwargs["font"]
		px = int(w * 0.5)
		py = int(h * 0.25)
		self.addSubWidget("titleText", Text, (px, py), self.message, font=f, \
			fontSize=22, anchor=(0, 0))

		if self.kwargs["description"]:
			px = int(w * 0.1)
			py = int(h * 0.4)
			self.addSubWidget("descText", Text, (px, py), \
				self.kwargs["description"], font=f, fontSize=18, \
				anchor=(-1, 0))

		py = int(h * 0.8)
		px = int(w * 0.75)
		if self.kwargs["negativeFct"]:
			self.addSubWidget("positiveText", Clickable_text, \
				(px, py), "oui", font=f, fontSize=18, anchor=(0, 0), \
				onClickFct=self.positiveAction)
			
			px = int(w * 0.25)
			self.addSubWidget("negativeText", Clickable_text, (px, py), \
				"non", font=f, fontSize=18, anchor=(0, 0), \
				onClickFct=self.negativeAction)
		else:
			self.addSubWidget("positiveText", Clickable_text, (px, py), "ok", \
				font=f, fontSize=18, anchor=(0, 0), \
				onClickFct=self.positiveAction)

	def negativeAction(self):
		"""
		This method is called when the second button is clicked. It destroys
			the menu and call negativeFct.
		"""

		self.destroy()
		self.kwargs["negativeFct"](*self.kwargs["negativeArgs"], \
			**self.kwargs["negativeKwargs"])

	def positiveAction(self):
		"""
		This method is called when the first button is clicked. It destroys
			the menu and call positiveFct.
		"""
		self.destroy()
		self.positiveFct(*self.kwargs["positiveArgs"], \
			**self.kwargs["positiveKwargs"])
