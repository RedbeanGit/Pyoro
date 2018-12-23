# -*- coding:utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 17/08/2018
	@version: 1.1
=========================
"""

import os

from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from gui.widget import Widget

class Eventable_widget(Widget):

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
		Eventable_widget.updateDefaultKwargs(kwargs)
		Widget.__init__(self, activity, pos, **kwargs)
		self.hovered = False
		self.clicked = False
		self.middleClicked = False
		self.rightClicked = False
		self.uneventableZones = []
		self.onClickSound = None

	def onEvent(self, event):
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
		self.hovered = True
		if self.kwargs["onHoverFct"]:
			self.kwargs["onHoverFct"](*self.kwargs["onHoverArgs"], **self.kwargs["onHoverKwargs"])

	def onEndHover(self):
		self.hovered = False



	def onClick(self):
		self.clicked = True

	def onMiddleClick(self):
		self.middleClicked = True

	def onRightClick(self):
		self.rightClicked = True

	def onMouseWheel(self, direction):
		if self.kwargs["onWheelFct"]:
			self.kwargs["onWheelFct"](direction, *self.kwargs["onWheelArgs"], **self.kwargs["onWheelKwargs"])



	def onClickOut(self):
		pass

	def onMiddleClickOut(self):
		pass

	def onRightClickOut(self):
		pass

	def onMouseWheelOut(self, direction):
		pass



	def onEndClick(self):
		if self.clicked:
			self.clicked = False
			if self.kwargs["onClickFct"]:
				self.kwargs["onClickFct"](*self.kwargs["onClickArgs"], **self.kwargs["onClickKwargs"])

	def onEndMiddleClick(self):
		if self.middleClicked:
			self.middleClicked = False
			if self.kwargs["onMiddleClickFct"]:
				self.kwargs["onMiddleClickFct"](*self.kwargs["onMiddleClickArgs"], **self.kwargs["onMiddleClickKwargs"])

	def onEndRightClick(self):
		if self.rightClicked:
			self.rightClicked = False
			if self.kwargs["onRightClickFct"]:
				self.kwargs["onRightClickFct"](*self.kwargs["onRightClickArgs"], **self.kwargs["onRightClickKwargs"])

	def onEndMouseWheel(self, direction):
		pass



	def onEndClickOut(self):
		if self.clicked:
			self.clicked = False

	def onEndMiddleClickOut(self):
		if self.middleClicked:
			self.middleClicked = False

	def onEndRightClickOut(self):
		if self.rightClicked:
			self.rightClicked = False

	def onEndMouseWheelOut(self, direction):
		pass



	def addUneventableZone(self, pos, size):
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
		if (pos[0], pos[1], size[0], size[1]) in self.uneventableZones:
			self.uneventableZones.remove((pos[0], pos[1], size[0], size[1]))

	def isInUneventableZone(self, pos):
		for uz in self.uneventableZones:
			if pos[0] >= uz[0] \
			and pos[0] <= uz[0] + uz[2] \
			and pos[1] >= uz[1] \
			and pos[1] <= uz[1] + uz[3]:
				return True
		return False