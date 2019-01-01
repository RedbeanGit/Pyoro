# -*- coding: utf-8 -*-

"""
Provide a menu to display when the game is paused.

Created on 18/08/2018
"""

from game.config import GUI_IMAGE_PATH

from gui.clickable_text import Clickable_text
from gui.menu_widget import Menu_widget
from gui.option_menu import Option_menu
from gui.text import Text

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import os


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
		fs = self.kwargs["fontSize"]

		px = int(w * 0.5)
		py = int(h * 0.2)
		self.addSubWidget("titleText", Text, (px, py), "Pause", \
			anchor=(0, 0), font=f, fontSize=fs + 15)
		py = int(h * 0.4)
		self.addSubWidget("resumeClickableText", Clickable_text, (px, py), \
			"continuer", anchor=(0, 0), font=f, fontSize=fs, onClickFct=self.destroy)
		py = int(h * 0.6)
		self.addSubWidget("optionClickableText", Clickable_text, (px, py), \
			"options", anchor=(0, 0), font=f, fontSize=fs, \
			onClickFct=self.openOptionMenu)
		py = int(h * 0.8)
		self.addSubWidget("quitClickableText", Clickable_text, (px, py), \
			"quitter", anchor=(0, 0), font=f, fontSize=fs, onClickFct=self.leaveLevel)

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

		rx, ry = self.getRealPos()
		x, y = x - rx, y - ry
		self.addSubWidget("option_menu", Option_menu, (x, y), \
			self.onOptionMenuDestroy, size = size, anchor = anchor)

	def onOptionMenuDestroy(self):
		"""
		This method is called when the Option_menu is destroyed.
		"""

		self.removeSubWidget("option_menu")
		self.activity.disableWidgets()
		self.config(enable = True)
