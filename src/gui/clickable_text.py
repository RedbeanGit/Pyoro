# -*- coding: utf-8 -*-

#   This file is part of Pyoro (A Python fan game).
#
#   Metawars is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Metawars is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
Provide a Clickable_text class used to create discreet buttons or links.

Created on 10/04/2018.
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from gui.eventable_widget import Eventable_widget
from gui.text import Text


class Clickable_text(Text, Eventable_widget):
	"""
	Create a text widget which will react on user events.
	"""

	DEFAULT_KWARGS = {
		"onClickTextColor": (200, 200, 200, 255),
		"onMiddleClickTextColor": (100, 100, 100, 255),
		"onRightClickTextColor": (220, 220, 220, 255),
		"onHoverTextColor": (230, 230, 230, 255),
		"disableTextColor": (240, 240, 240, 235)
	}

	def __init__(self, activity, pos, text, **kwargs):
		"""
		Initialize a new Text objects.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The default position of the widget in a (x, y) tuple where
			x and y are integers.

		:type text: str
		:param text: The text to render.

		onClickTextColor, onMiddleClickTextColor, onRightClickTextColor,
		onHoverTextColor, disableTextColor, can be defined.
		"""

		Clickable_text.updateDefaultKwargs(kwargs)
		Text.__init__(self, activity, pos, text, **kwargs)
		Eventable_widget.__init__(self, activity, pos, **self.kwargs)

	def update(self, deltaTime):
		"""
		Update the clickable text by redrawing it on the window with the
			appropriate color.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last call of this method (in
			seconds).
		"""

		if not self.kwargs["enable"]:
			self.font.fgcolor = self.kwargs["disableTextColor"]
		elif self.clicked:
			self.font.fgcolor = self.kwargs["onClickTextColor"]
		elif self.rightClicked:
			self.font.fgcolor = self.kwargs["onRightClickTextColor"]
		elif self.middleClicked:
			self.font.fgcolor = self.kwargs["onMiddleClickTextColor"]
		elif self.hovered:
			self.font.fgcolor = self.kwargs["onHoverTextColor"]
		else:
			self.font.fgcolor = self.kwargs["textColor"]
		Text.update(self, deltaTime)