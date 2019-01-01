# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 20/08/2018
	@version: 1.1
=========================
"""

import os
from pygame.locals import MOUSEMOTION

from game.config import GUI_IMAGE_PATH
from gui.eventable_widget import Eventable_widget
from gui.image_transformer import stretchImage

class Setting_bar(Eventable_widget):

	DEFAULT_KWARGS = {
		"lineThickness": 16,
		"cursorWidth": 16,

		"lineImageBorderSize": 4,
		"cursorImageBorderSize": 4,

		"value": 0,

		"lineImage": os.path.join(GUI_IMAGE_PATH, "setting bar", "line.png"),
		"onHoverLineImage": os.path.join(GUI_IMAGE_PATH, "setting bar", "line_hover.png"),
		"onClickLineImage": os.path.join(GUI_IMAGE_PATH, "setting bar", "line_click.png"),
		"onMiddleClickLineImage": os.path.join(GUI_IMAGE_PATH, "setting bar", "line_middle_click.png"),
		"onRightClickLineImage": os.path.join(GUI_IMAGE_PATH, "setting bar", "line_right_click.png"),
		"disableLineImage": os.path.join(GUI_IMAGE_PATH, "setting bar", "line_disable.png"),

		"cursorImage": os.path.join(GUI_IMAGE_PATH, "setting bar", "cursor.png"),
		"onHoverCursorImage": os.path.join(GUI_IMAGE_PATH, "setting bar", "cursor_hover.png"),
		"onClickCursorImage": os.path.join(GUI_IMAGE_PATH, "setting bar", "cursor_click.png"),
		"onMiddleClickCursorImage": os.path.join(GUI_IMAGE_PATH, "setting bar", "cursor_middle_click.png"),
		"onRightClickCursorImage": os.path.join(GUI_IMAGE_PATH, "setting bar", "cursor_right_click.png"),
		"disableCursorImage": os.path.join(GUI_IMAGE_PATH, "setting bar", "cursor_disable.png")
	}

	def __init__(self, activity, pos, **kwargs):
		Setting_bar.updateDefaultKwargs(kwargs)
		Eventable_widget.__init__(self, activity, pos, **kwargs)

		self.lineImage = None
		self.onHoverLineImage = None
		self.onClickLineImage = None
		self.onMiddleClickLineImage = None
		self.onRightClickLineImage = None
		self.disableLineImage = None

		self.cursorImage = None
		self.onHoverCursorImage = None
		self.onClickCursorImage = None
		self.onMiddleClickCursorImage = None
		self.onRightClickCursorImage = None
		self.disableCursorImage = None

		self.cursorPos = self.getCursorPosWithValue(self.kwargs["value"])

		self.loadLineImages()
		self.loadCursorImages()

	def loadLineImages(self):
		imageNames = ("lineImage", "onHoverLineImage", "onClickLineImage", "onMiddleClickLineImage", "onRightClickLineImage", "disableLineImage")
		for imageName in imageNames:
			if self.kwargs[imageName]:
				image = stretchImage( \
					self.activity.window.getImage(self.kwargs[imageName]), \
					(self.kwargs["size"][0], self.kwargs["lineThickness"]), \
					self.kwargs["lineImageBorderSize"])

				self.__setattr__(imageName, image)

	def loadCursorImages(self):
		imageNames = ("cursorImage", "onHoverCursorImage", "onClickCursorImage", "onMiddleClickCursorImage", "onRightClickCursorImage", "disableCursorImage")
		for imageName in imageNames:
			if self.kwargs[imageName]:
				image = stretchImage( \
					self.activity.window.getImage(self.kwargs[imageName]), \
					(self.kwargs["cursorWidth"], self.kwargs["size"][1]), \
					self.kwargs["cursorImageBorderSize"])
				self.__setattr__(imageName, image)

	def update(self, deltaTime):
		self.drawLine()
		self.drawCursor()

	def drawLine(self):
		if not self.kwargs["enable"] and self.disableLineImage:
			self.activity.window.drawImage(self.disableLineImage, self.getLinePos())
		if self.clicked and self.onClickLineImage:
			self.activity.window.drawImage(self.onClickLineImage, self.getLinePos())
		elif self.rightClicked and self.onRightClickLineImage:
			self.activity.window.drawImage(self.onRightClickLineImage, self.getLinePos())
		elif self.middleClicked and self.onMiddleClickLineImage:
			self.activity.window.drawImage(self.onMiddleClickLineImage, self.getLinePos())
		elif self.hovered and self.onHoverLineImage:
			self.activity.window.drawImage(self.onHoverLineImage, self.getLinePos())
		elif self.lineImage:
			self.activity.window.drawImage(self.lineImage, self.getLinePos())

	def drawCursor(self):
		if not self.kwargs["enable"] and self.disableCursorImage:
			self.activity.window.drawImage(self.disableCursorImage, self.getCursorPos())
		if self.clicked and self.onClickCursorImage:
			self.activity.window.drawImage(self.onClickCursorImage, self.getCursorPos())
		elif self.rightClicked and self.onRightClickCursorImage:
			self.activity.window.drawImage(self.onRightClickCursorImage, self.getCursorPos())
		elif self.middleClicked and self.onMiddleClickCursorImage:
			self.activity.window.drawImage(self.onMiddleClickCursorImage, self.getCursorPos())
		elif self.hovered and self.onHoverCursorImage:
			self.activity.window.drawImage(self.onHoverCursorImage, self.getCursorPos())
		elif self.cursorImage:
			self.activity.window.drawImage(self.cursorImage, self.getCursorPos())

	def getLinePos(self):
		realPos = self.getRealPos()
		return [realPos[0], realPos[1] + self.kwargs["size"][1] // 2 - self.kwargs["lineThickness"] // 2]

	def getCursorPos(self):
		realPos = self.getRealPos()
		return [self.cursorPos - self.kwargs["cursorWidth"] // 2, realPos[1]]

	def onEvent(self, event):
		Eventable_widget.onEvent(self, event)
		if self.kwargs["enable"] and self.clicked:
			if event.type == MOUSEMOTION:
				realPos = self.getRealPos()
				if event.pos[0] >= realPos[0] + self.kwargs["cursorWidth"] / 2 and event.pos[0] <= realPos[0] + self.kwargs["size"][0] - self.kwargs["cursorWidth"] / 2:
					self.cursorPos = event.pos[0]
				elif event.pos[0] < realPos[0] + self.kwargs["cursorWidth"] / 2:
					self.cursorPos = realPos[0] + self.kwargs["cursorWidth"] / 2
				else:
					self.cursorPos = realPos[0] + self.kwargs["size"][0] - self.kwargs["cursorWidth"] / 2

	def getValue(self):
		realPos = self.getRealPos()
		if self.kwargs["size"][0] - self.kwargs["cursorWidth"] != 0:
			return (self.cursorPos - realPos[0] - self.kwargs["cursorWidth"] / 2) / (self.kwargs["size"][0] - self.kwargs["cursorWidth"])
		return 0.5

	def getCursorPosWithValue(self, value):
		return value * (self.kwargs["size"][0] - self.kwargs["cursorWidth"]) + self.kwargs["cursorWidth"] / 2 + self.getRealPos()[0]

	def config(self, **kwargs):
		Eventable_widget.config(self, **kwargs)

		if "cursorImageBorderSize" in kwargs or \
			"cursorWidth" in kwargs or \
			"cursorImage" in kwargs or \
			"onHoverCursorImage" in kwargs or \
			"onClickCursorImage" in kwargs or \
			"onMiddleClickCursorImage" in kwargs or \
			"onRightClickCursorImage" in kwargs or \
			"disableCursorImage" in kwargs:
			self.loadCursorImages()

		if "lineImageBorderSize" in kwargs or \
			"lineThickness" in kwargs or \
			"lineImage" in kwargs or \
			"onHoverLineImage" in kwargs or \
			"onClickLineImage" in kwargs or \
			"onMiddleClickLineImage" in kwargs or \
			"onRightClickLineImage" in kwargs or \
			"disableLineImage" in kwargs:
			self.loadLineImages()

		if "value" in kwargs:
			self.cursorPos = self.getCursorPosWithValue(kwargs["value"])
