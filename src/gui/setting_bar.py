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
Provide a Setting_bar class.

Created on 20/08/2018.
"""

import os
from pygame.locals import MOUSEMOTION

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH
from gui.eventable_widget import Eventable_widget
from gui.image_transformer import stretchImage


class Setting_bar(Eventable_widget):
	"""
	Create a widget allowing the player to choose an approximate value
		within [0; 1].
	"""

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
		"""
		Initialize a new Text objects.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The default position of the widget in a (x, y) tuple where
			x and y are integers.

		lineThickness, cursorWidth, lineImageBorderSize,
		cursorImageBorderSize, value, lineImage, onHoverLineImage,
		onClickLineImage, onMiddleClickLineImage, onRightClickLineImage,
		disableLineImage, cursorImage, onHoverCursorImage,
		onMiddleClickCursorImage, onRightClickCursorImage and
		disableCursorImage can be defined.
		"""

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
		"""
		Load the line images and stretch them to the right size.
		"""

		imageNames = ("lineImage", "onHoverLineImage", "onClickLineImage", \
			"onMiddleClickLineImage", "onRightClickLineImage", \
			"disableLineImage")

		for imageName in imageNames:
			if self.kwargs[imageName]:
				image = stretchImage( \
					self.activity.window.getImage(self.kwargs[imageName]), \
					(self.kwargs["size"][0], self.kwargs["lineThickness"]), \
					self.kwargs["lineImageBorderSize"])

				self.__setattr__(imageName, image)

	def loadCursorImages(self):
		"""
		Load the cursor images and stretch them to the right size.
		"""

		imageNames = ("cursorImage", "onHoverCursorImage", \
			"onClickCursorImage", "onMiddleClickCursorImage", \
			"onRightClickCursorImage", "disableCursorImage")

		for imageName in imageNames:
			if self.kwargs[imageName]:
				image = stretchImage( \
					self.activity.window.getImage(self.kwargs[imageName]), \
					(self.kwargs["cursorWidth"], self.kwargs["size"][1]), \
					self.kwargs["cursorImageBorderSize"])
				self.__setattr__(imageName, image)

	def update(self, deltaTime):
		"""
		Draw the line and the cursor.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last call of this method (in
			seconds).
		"""

		self.drawLine()
		self.drawCursor()

	def drawLine(self):
		"""
		Draw the right line image according to the widget state.
		"""

		if not self.kwargs["enable"] and self.disableLineImage:
			self.activity.window.drawImage(self.disableLineImage, \
				self.getLinePos())
		
		if self.clicked and self.onClickLineImage:
			self.activity.window.drawImage(self.onClickLineImage, \
				self.getLinePos())
		
		elif self.rightClicked and self.onRightClickLineImage:
			self.activity.window.drawImage(self.onRightClickLineImage, \
				self.getLinePos())
		
		elif self.middleClicked and self.onMiddleClickLineImage:
			self.activity.window.drawImage(self.onMiddleClickLineImage, \
				self.getLinePos())
		
		elif self.hovered and self.onHoverLineImage:
			self.activity.window.drawImage(self.onHoverLineImage, \
				self.getLinePos())
		
		elif self.lineImage:
			self.activity.window.drawImage(self.lineImage, \
				self.getLinePos())

	def drawCursor(self):
		"""
		Draw the right line image according to the widget state.
		"""

		if not self.kwargs["enable"] and self.disableCursorImage:
			self.activity.window.drawImage(self.disableCursorImage, \
				self.getCursorPos())
		
		if self.clicked and self.onClickCursorImage:
			self.activity.window.drawImage(self.onClickCursorImage, \
				self.getCursorPos())
		
		elif self.rightClicked and self.onRightClickCursorImage:
			self.activity.window.drawImage(self.onRightClickCursorImage, \
				self.getCursorPos())
		
		elif self.middleClicked and self.onMiddleClickCursorImage:
			self.activity.window.drawImage(self.onMiddleClickCursorImage, \
				self.getCursorPos())
		
		elif self.hovered and self.onHoverCursorImage:
			self.activity.window.drawImage(self.onHoverCursorImage, \
				self.getCursorPos())
		
		elif self.cursorImage:
			self.activity.window.drawImage(self.cursorImage, \
				self.getCursorPos())

	def getLinePos(self):
		"""
		Compute the position of the upper left corner of the line.

		:rtype: list
		:returns: A [x, y] list where x and y are both integers.
		"""

		realPos = self.getRealPos()
		return [realPos[0], realPos[1] + self.kwargs["size"][1] // 2 \
			- self.kwargs["lineThickness"] // 2]

	def getCursorPos(self):
		"""
		Compute the position of the upper left corner of the cursor.

		:rtype: list
		:returns: A [x, y] list where x and y are both integers.
		"""

		realPos = self.getRealPos()
		return [self.cursorPos - self.kwargs["cursorWidth"] // 2, realPos[1]]

	def onEvent(self, event):
		"""
		This method is called on all user events detected by Pygame.

		:type event: pygame.event.Event
		:param event: The event to handle.
		"""

		Eventable_widget.onEvent(self, event)
		if self.kwargs["enable"] and self.clicked:
			if event.type == MOUSEMOTION:
				realPos = self.getRealPos()
				
				if event.pos[0] >= realPos[0] \
				+ self.kwargs["cursorWidth"] / 2 and event.pos[0] \
				<= realPos[0] + self.kwargs["size"][0] \
				- self.kwargs["cursorWidth"] / 2:
					self.cursorPos = event.pos[0]
				
				elif event.pos[0] < realPos[0] \
				+ self.kwargs["cursorWidth"] / 2:
					self.cursorPos = realPos[0] \
					+ self.kwargs["cursorWidth"] / 2
				
				else:
					self.cursorPos = realPos[0] + self.kwargs["size"][0] \
					- self.kwargs["cursorWidth"] / 2

	def getValue(self):
		"""
		Return a value between 0 and 1 from the position of the cursor on the
			line.

		:rtype: float
		:returns: The value of the setting bar.
		"""

		realPos = self.getRealPos()
		if self.kwargs["size"][0] - self.kwargs["cursorWidth"] != 0:
			return (self.cursorPos - realPos[0] - self.kwargs["cursorWidth"] \
				/ 2) / (self.kwargs["size"][0] - self.kwargs["cursorWidth"])
		return 0.5

	def getCursorPosWithValue(self, value):
		"""
		Return the horizontal position of the upper left corner of the cursor
			from a give value.

		:type value: float
		:param value: Any float number between 0 and 1.

		:rtype: float
		:returns: The absolute x position of the cursor.
		"""

		return value * (self.kwargs["size"][0] - self.kwargs["cursorWidth"]) \
			+ self.kwargs["cursorWidth"] / 2 + self.getRealPos()[0]

	def config(self, **kwargs):
		"""
		Change some kwargs of the widget (cursorWidth, cursorImage, ...).
		"""
		
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
