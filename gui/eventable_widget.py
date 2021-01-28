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
Provide an Eventable_widget base class to manage user events and inputs.

Created on 17/08/2018.
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from gui.widget import Widget


class Eventable_widget(Widget):
	"""
	This class exists to be subclassed by widgets which have to be able to
		handle user events.
	"""

	DEFAULT_KWARGS = {
		"enable": True,

		"onClickFct": None,
		"onClickArgs": (),
		"onClickKwargs": {},

		"onHoverFct": None,
		"onHoverArgs": (),
		"onHoverKwargs": {},

		"onMiddleClickFct": None,
		"onMiddleClickArgs": (),
		"onMiddleClickKwargs": {},

		"onRightClickFct": None,
		"onRightClickArgs": (),
		"onRightClickKwargs": {},

		"onWheelFct": None,
		"onWheelArgs": (),
		"onWheelKwargs": {},

		"onClickSound": os.path.join("data", "audio", "sounds", "widget_click.wav")
	}

	def __init__(self, activity, pos, **kwargs):
		"""
		Initialize a new Button object.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The default position of the widget in a (x, y) tuple where
			x and y are integers.

		onClickFct, onClickArgs, onClickKwargs,
		onHoverFct, onHoverArgs, onHoverKwargs,
		onMiddleClickFct, onMiddleClickArgs, onMiddleClickKwargs,
		onRightClickFct, onRightClickArgs, onRightClickKwargs,
		onWheelFct, onWheelArgs, onWheelKwargs,
		and onClickSound can be defined.
		"""

		Eventable_widget.updateDefaultKwargs(kwargs)
		Widget.__init__(self, activity, pos, **kwargs)
		self.hovered = False
		self.clicked = False
		self.middleClicked = False
		self.rightClicked = False
		self.uneventableZones = []
		self.onClickSound = None

	def onEvent(self, event):
		"""
		This method is called on all user events detected by Pygame.

		:type event: pygame.event.Event
		:param event: The event to handle.
		"""

		if self.kwargs["enable"]:
			if event.type == MOUSEMOTION:
				if not self.isInUneventableZone(event.pos):
					if self.isInWidget(event.pos):  self.onHover()
					else:	self.onEndHover()

			elif event.type == MOUSEBUTTONDOWN:
				if not self.isInUneventableZone(event.pos):
					if self.isInWidget(event.pos):
						if event.button == 1:   self.onClick()
						elif event.button == 2: self.onMiddleClick()
						elif event.button == 3: self.onRightClick()
						elif event.button == 4: self.onMouseWheel(1)
						elif event.button == 5: self.onMouseWheel(-1)
					else:
						if event.button == 1:   self.onClickOut()
						elif event.button == 2: self.onMiddleClickOut()
						elif event.button == 3: self.onRightClickOut()
						elif event.button == 4: self.onMouseWheelOut(1)
						elif event.button == 5: self.onMouseWheelOut(-1)

			elif event.type == MOUSEBUTTONUP:
				if not self.isInUneventableZone(event.pos):
					if self.isInWidget(event.pos):
						if event.button == 1:   self.onEndClick()
						elif event.button == 2: self.onEndMiddleClick()
						elif event.button == 3: self.onEndRightClick()
						elif event.button == 4: self.onEndMouseWheel(1)
						elif event.button == 5: self.onEndMouseWheel(-1)
					else:
						if event.button == 1:   self.onEndClickOut()
						elif event.button == 2: self.onEndMiddleClickOut()
						elif event.button == 3: self.onEndRightClickOut()
						elif event.button == 4: self.onEndMouseWheelOut(1)
						elif event.button == 5: self.onEndMouseWheelOut(-1)

	def onHover(self):
		"""
		Set hovered state to True and call onHoverFct.
		"""

		self.hovered = True
		if self.kwargs["onHoverFct"]:
			self.kwargs["onHoverFct"](*self.kwargs["onHoverArgs"], **self.kwargs["onHoverKwargs"])

	def onEndHover(self):
		"""
		Set hovered state to False.
		"""

		self.hovered = False

	def onClick(self):
		"""
		Set clicked state to True.
		"""

		self.clicked = True

	def onMiddleClick(self):
		"""
		Set middleClicked state to True.
		"""

		self.middleClicked = True

	def onRightClick(self):
		"""
		Set rightClicked state to True.
		"""

		self.rightClicked = True

	def onMouseWheel(self, direction):
		"""
		Call onWheelFct.
		"""

		if self.kwargs["onWheelFct"]:
			self.kwargs["onWheelFct"](direction, *self.kwargs["onWheelArgs"], **self.kwargs["onWheelKwargs"])

	def onClickOut(self):
		"""
		Do nothing by default. This method has to be overridden.
		"""
		pass

	def onMiddleClickOut(self):
		"""
		Do nothing by default. This method has to be overridden.
		"""
		pass

	def onRightClickOut(self):
		"""
		Do nothing by default. This method has to be overridden.
		"""
		pass

	def onMouseWheelOut(self, direction):
		"""
		Do nothing by default. This method has to be overridden.
		"""
		pass

	def onEndClick(self):
		"""
		Set clicked state to False and call onClickFct.
		"""

		if self.clicked:
			self.clicked = False
			if self.kwargs["onClickFct"]:
				self.kwargs["onClickFct"](*self.kwargs["onClickArgs"], **self.kwargs["onClickKwargs"])

	def onEndMiddleClick(self):
		"""
		Set middleClicked state to False and call onMiddleClickFct.
		"""

		if self.middleClicked:
			self.middleClicked = False
			if self.kwargs["onMiddleClickFct"]:
				self.kwargs["onMiddleClickFct"](*self.kwargs["onMiddleClickArgs"], **self.kwargs["onMiddleClickKwargs"])

	def onEndRightClick(self):
		"""
		Set rightClicked state to False and call onRightClickFct.
		"""

		if self.rightClicked:
			self.rightClicked = False
			if self.kwargs["onRightClickFct"]:
				self.kwargs["onRightClickFct"](*self.kwargs["onRightClickArgs"], **self.kwargs["onRightClickKwargs"])

	def onEndMouseWheel(self, direction):
		"""
		Do nothing by default. This method has to be overridden.
		"""
		pass

	def onEndClickOut(self):
		"""
		Set clicked state to False.
		"""

		if self.clicked:
			self.clicked = False

	def onEndMiddleClickOut(self):
		"""
		Set middleClicked state to False.
		"""

		if self.middleClicked:
			self.middleClicked = False

	def onEndRightClickOut(self):
		"""
		Set rightClicked state to False.
		"""

		if self.rightClicked:
			self.rightClicked = False

	def onEndMouseWheelOut(self, direction):
		"""
		Do nothing by default. This method has to be overridden.
		"""
		pass

	def addUneventableZone(self, pos, size):
		"""
		Add a zone where mouse events will have no effects for this widget.

		:type pos: tuple
		:param pos: A (x, y) tuple representing the top left corner of the
			uneventable zone (in pixel).

		:type size: tuple
		:param size: A (w, h) tuple representing the size in pixel of the
			uneventable zone.

		:rtype: tuple
		:returns: A (x, y, w, h) tuple representing the uneventable zone
			created.
		"""

		realPos = self.getRealPos()

		if pos[0] >= realPos[0] \
		and pos[0] <= realPos[0] + self.kwargs["size"][0] \
		and pos[1] >= realPos[1] \
		and pos[1] <= realPos[1] + self.kwargs["size"][1]:
			if pos[0] + size[0] > realPos[0] + self.kwargs["size"][0]:
				size[0] = self.realPos[0] + self.kwargs["size"][0] - pos[0]
			if pos[1] + size[1] > realPos[1] + self.kwargs["size"][1]:
				size[1] = self.realPos[1] + self.kwargs["size"][1] - pos[1]
			
			self.uneventableZones.append((pos[0], pos[1], size[0], size[1]))

			return (pos[0], pos[1], size[0], size[1])
		else:
			print("[WARNING] [Eventable_Widget.addUneventableZone] The zone exceeds the widget")

	def removeUneventableZone(self, pos, size):
		"""
		Remove an uneventable zone.

		:type pos: tuple
		:param pos: A (x, y) tuple representing the top left corner of the
			uneventable zone (in pixel).

		:type size: tuple
		:param size: A (w, h) tuple representing the size in pixel of the
			uneventable zone.
		"""

		if (pos[0], pos[1], size[0], size[1]) in self.uneventableZones:
			self.uneventableZones.remove((pos[0], pos[1], size[0], size[1]))

	def isInUneventableZone(self, pos):
		"""
		Check if a position is within an eventable zone.

		:type pos: tuple
		:param pos: A (x, y) tuple representing the position to check.

		:rtype: bool
		:returns: True if the position is within an uneventable zone.
		"""

		for uz in self.uneventableZones:
			if pos[0] >= uz[0] \
			and pos[0] <= uz[0] + uz[2] \
			and pos[1] >= uz[1] \
			and pos[1] <= uz[1] + uz[3]:
				return True
		return False