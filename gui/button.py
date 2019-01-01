# -*- coding: utf-8 -*-

"""
Provide a class to create button widgets with update on click and on hover.

Created on 18/08/2018
"""

from game.config import GUI_IMAGE_PATH

from gui.eventable_widget import Eventable_widget
from gui.image_transformer import resizeImage
from gui.text import Text

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import os


class Button(Eventable_widget):
	"""
	A simple button widget.
	"""

	DEFAULT_KWARGS = {
		"text": "",
		"textKwargs": {
			"anchor": (0, 0)
		},
		"textAnchor": (0, 0),
		"backgroundImage": os.path.join(GUI_IMAGE_PATH, "button", "button.png"),
		"onHoverBackgroundImage": os.path.join(GUI_IMAGE_PATH, "button", \
			"button_hover.png"),
		"onClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "button", \
			"button_click.png"),
		"onMiddleClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "button", \
			"button_middle_click.png"),
		"onRightClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "button", \
			"button_right_click.png"),
		"disableBackgroundImage": os.path.join(GUI_IMAGE_PATH, "button", \
			"button_disable.png")
	}

	def __init__(self, activity, pos, **kwargs):
		"""
		Initialize a new Button object.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The default position of the button in a (x, y) tuple where
			x and y are integers.
		"""

		Button.updateDefaultKwargs(kwargs)
		Button.updateDefaultTextKwargs(kwargs)
		Eventable_widget.__init__(self, activity, pos, **kwargs)
		self.backgroundImages = {}
		self.text = Text(self.activity, self.getTextPos(), self.kwargs["text"], \
			**self.kwargs["textKwargs"])
		self.loadBackgroundImages()

	@classmethod
	def updateDefaultTextKwargs(cls, kwargs):
		for key, value in cls.DEFAULT_KWARGS["textKwargs"].items():
			if key not in kwargs["textKwargs"]:
				kwargs["textKwargs"][key] = value

	def loadBackgroundImages(self):
		"""
		Load the button background images.
		"""

		eventNames = (
			"",
			"onHover",
			"onClick",
			"onMiddleClick",
			"onRightClick",
			"disable"
		)

		for eventName in eventNames:
			if eventName:
				backgroundName = eventName + "BackgroundImage"
			else:
				backgroundName = "backgroundImage"
			self.backgroundImages[eventName] = resizeImage(
				self.activity.window.getImage(self.kwargs[backgroundName]), \
				self.kwargs["size"])

	def update(self, deltaTime):
		"""
		Redraw the button with the best background for the current event.
		"""

		eventName = ""
		if (not self.kwargs["enable"]):
			eventName = "disable"
		elif self.clicked:
			eventName = "onClick"
		elif self.rightClicked:
			eventName = "onRightClick"
		elif self.middleClicked:
			eventName = "onMiddleClick"
		elif self.hovered:
			eventName = "onHover"

		if eventName in self.backgroundImages:
			self.activity.window.drawImage(self.backgroundImages[eventName], \
				self.getRealPos())

		self.text.update(deltaTime)
		Eventable_widget.update(self, deltaTime)

	def config(self, **kwargs):
		"""
		Change some attributes of this button and update it.
		"""

		Eventable_widget.config(self, **kwargs)
		if "text" in kwargs:
			self.text.text = kwargs["text"]
		if "textAnchor" in kwargs:
			self.text.pos = self.getTextPos()
		if "textKwargs" in kwargs:
			self.text.config(**kwargs["textKwargs"])

		# If any background is modified
		if "backgroundImage" in kwargs \
		or "onHoverBackgroundImage" in kwargs \
		or "onClickBackgroundImage" in kwargs \
		or "onMiddleClickBackgroundImage" in kwargs \
		or "onRightClickBackgroundImage" in kwargs \
		or "disableBackgroundImage" in kwargs:
			self.loadBackgroundImages()

	def getTextPos(self):
		x, y = self.getRealPos()
		w, h = self.kwargs["size"]
		ax, ay = self.kwargs["textAnchor"]
		return (x + w * (ax + 1) / 2, y + h * (ay + 1) / 2)
