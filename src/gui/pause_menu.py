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
Provide a menu to display when the game is paused.

Created on 18/08/2018
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH

from gui.clickable_text import Clickable_text
from gui.menu_widget import Menu_widget
from gui.option_menu import Option_menu
from gui.text import Text


class Pause_menu(Menu_widget):
	"""
	A menu to display when the game is paused.
	"""

	DEFAULT_KWARGS = {
		"fontSize": 20,
		"font": os.path.join(GUI_IMAGE_PATH, "font.ttf")
	}

	def __init__(self, activity, pos, resumeFct, quitFct, **kwargs):
		"""
		Initialize a new Pause_menu object.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The position of the widget in a (x, y) tuple where x and y
			are integers.

		:type resumeFct: callable
		:param resumeFct: A function, class or method which can be called on click
			on the "resume" button.

		:type quitFct: callable
		:param quitFct: A function, class or method which can be called on click
			on the "quit" button.
		"""

		Pause_menu.updateDefaultKwargs(kwargs)
		Menu_widget.__init__(self, activity, pos, **kwargs)

		self.resumeFct = resumeFct
		self.quitFct = quitFct

	def initWidgets(self):
		"""
		Create widgets displayed in this dialog.
		"""

		realPos = self.getRealPos()
		w, h = self.kwargs["size"]
		f = self.kwargs["font"]
		ts = self.kwargs["fontSize"]; ms = ts - 3

		px = int(w * 0.5)
		py = int(h * 0.2)
		self.addSubWidget("titleText", Text, (px, py), "Pause", \
			anchor=(0, 0), font=f, fontSize=ts)
		py = int(h * 0.4)
		self.addSubWidget("resumeClickableText", Clickable_text, (px, py), \
			"continuer", anchor=(0, 0), font=f, fontSize=ms, onClickFct=self.destroy)
		py = int(h * 0.6)
		self.addSubWidget("optionClickableText", Clickable_text, (px, py), \
			"options", anchor=(0, 0), font=f, fontSize=ms, \
			onClickFct=self.openOptionMenu)
		py = int(h * 0.8)
		self.addSubWidget("quitClickableText", Clickable_text, (px, py), \
			"quitter", anchor=(0, 0), font=f, fontSize=ms, onClickFct=self.leaveLevel)

	def destroy(self):
		"""
		Destroy the widget and its subwidgets, then call resumeFct.
		"""

		Menu_widget.destroy(self)
		self.resumeFct()

	def leaveLevel(self):
		"""
		Destroy the widget and its subwidgets, then call quitFct.
		"""

		Menu_widget.destroy(self)
		self.quitFct()

	def openOptionMenu(self):
		"""
		Create an Option_menu.
		"""

		layout = self.activity.layout
		x, y = layout.getWidgetPos("option_menu")
		size = layout.getWidgetSize("option_menu")
		anchor = layout.getWidgetAnchor("option_menu")
		fsize = layout.getFontSize("option_menu")

		rx, ry = self.getRealPos()
		x, y = x - rx, y - ry
		self.addSubWidget("option_menu", Option_menu, (x, y), \
			self.onOptionMenuDestroy, size = size, anchor = anchor, \
			fontSize = fsize)

	def onOptionMenuDestroy(self):
		"""
		This method is called when the Option_menu is destroyed.
		"""

		self.removeSubWidget("option_menu")
		self.activity.disableWidgets()
		self.config(enable = True)
