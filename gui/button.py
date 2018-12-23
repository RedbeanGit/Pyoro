# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 18/08/2018
	@version: 1.1
=========================
"""

import os

from game.config import GUI_IMAGE_PATH
from gui.clickable_text import Clickable_text
from gui.image_transformer import Image_transformer

class Button(Clickable_text):
	""" Simple Button widget """

	DEFAULT_KWARGS = {
		"text": "",
		"backgroundAnchor": (0, 0),

		"backgroundImage": os.path.join(GUI_IMAGE_PATH, "button", "button.png"),
		"onHoverBackgroundImage": os.path.join(GUI_IMAGE_PATH, "button", "button_hover.png"),
		"onClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "button", "button_click.png"),
		"onMiddleClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "button", "button_middle_click.png"),
		"onRightClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "button", "button_right_click.png"),
		"disableBackgroundImage": os.path.join(GUI_IMAGE_PATH, "button", "button_disable.png")
	}

	def __init__(self, activity, pos, **kwargs):
		Button.updateDefaultKwargs(kwargs)
		text = kwargs.pop("text")
		Clickable_text.__init__(self, activity, pos, text, **kwargs)

		self.backgroundImage = None
		self.onHoverBackgroundImage = None
		self.onClickBackgroundImage = None
		self.onMiddleClickBackgroundImage = None
		self.onRightClickBackgroundImage = None
		self.disableBackgroundImage = None

		self.loadBackgroundImages()

	def loadBackgroundImages(self):
		if self.kwargs["backgroundImage"]:
			self.backgroundImage = Image_transformer.resize(self.activity.window.getImage(self.kwargs["backgroundImage"]), self.kwargs["size"])
		if self.kwargs["onHoverBackgroundImage"]:
			self.onHoverBackgroundImage = Image_transformer.resize(self.activity.window.getImage(self.kwargs["onHoverBackgroundImage"]), self.kwargs["size"])
		if self.kwargs["onClickBackgroundImage"]:
			self.onClickBackgroundImage = Image_transformer.resize(self.activity.window.getImage(self.kwargs["onClickBackgroundImage"]), self.kwargs["size"])
		if self.kwargs["onMiddleClickBackgroundImage"]:
			self.onMiddleClickBackgroundImage = Image_transformer.resize(self.activity.window.getImage(self.kwargs["onMiddleClickBackgroundImage"]), self.kwargs["size"])
		if self.kwargs["onRightClickBackgroundImage"]:
			self.onRightClickBackgroundImage = Image_transformer.resize(self.activity.window.getImage(self.kwargs["onRightClickBackgroundImage"]), self.kwargs["size"])
		if self.kwargs["disableBackgroundImage"]:
			self.disableBackgroundImage = Image_transformer.resize(self.activity.window.getImage(self.kwargs["disableBackgroundImage"]), self.kwargs["size"])

	def update(self, deltaTime):
		if (not self.kwargs["enable"]) and self.disableBackgroundImage:
			self.activity.window.drawImage(self.disableBackgroundImage, self.getBackgroundPos())
		elif self.clicked and self.onClickBackgroundImage:
			self.activity.window.drawImage(self.onClickBackgroundImage, self.getBackgroundPos())
		elif self.rightClicked and self.onRightClickBackgroundImage:
			self.activity.window.drawImage(self.onRightClickBackgroundImage, self.getBackgroundPos())
		elif self.middleClicked and self.onMiddleClickBackgroundImage:
			self.activity.window.drawImage(self.onMiddleClickBackgroundImage, self.getBackgroundPos())
		elif self.hovered and self.onHoverBackgroundImage:
			self.activity.window.drawImage(self.onHoverBackgroundImage, self.getBackgroundPos())
		elif self.backgroundImage:
			self.activity.window.drawImage(self.backgroundImage, self.getBackgroundPos())
		size = self.kwargs["size"]
		Clickable_text.update(self, deltaTime)
		self.kwargs["size"] = size

	def config(self, **kwargs):
		Clickable_text.config(self, **kwargs)
		if "text" in kwargs:
			self.text = kwargs["text"]
		if "backgroundImage" in kwargs \
		or "onHoverBackgroundImage" in kwargs \
		or "onClickBackgroundImage" in kwargs \
		or "onMiddleClickBackgroundImage" in kwargs \
		or "onRightClickBackgroundImage" in kwargs \
		or "disableBackgroundImage" in kwargs:
			self.loadBackgroundImages()

	def getBackgroundPos(self):
		return [
			int(self.pos[0] - self.kwargs["size"][0] * (self.kwargs["backgroundAnchor"][0] + self.kwargs["anchor"][0] + 1) / 2), \
			int(self.pos[1] - self.kwargs["size"][1] * (self.kwargs["backgroundAnchor"][1] + self.kwargs["anchor"][1] + 1) / 2)
		]