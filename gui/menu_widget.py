# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 08/10/2018
	@version: 1.1
=========================
"""

import os

from game.config import GUI_IMAGE_PATH
from gui.image_transformer import Image_transformer
from gui.widget import Widget

class Menu_widget(Widget):

	DEFAULT_KWARGS = {
		"backgroundImage": os.path.join(GUI_IMAGE_PATH, "frame.png")
	}

	def __init__(self, activity, pos, **kwargs):
		Menu_widget.updateDefaultKwargs(kwargs)
		Widget.__init__(self, activity, pos, **kwargs)

		self.subWidgets = {}
		self.backgroundImage = None
		self.activity.disableWidgets()
		self.loadBackgroundImage()
		self.initWidgets()

	def loadBackgroundImage(self):
		if self.kwargs["backgroundImage"]:
			self.backgroundImage = Image_transformer.stretch(self.activity.window.getImage(self.kwargs["backgroundImage"]), self.kwargs["size"], 5)

	def initWidgets(self):
		pass

	def addSubWidget(self, widgetName, widgetType, pos, *widgetArgs, **widgetKwargs):
		if widgetName in self.subWidgets:
			print("[WARNING] [Menu_widget.addSubWidget] A widget called \"{}\" already exists in this Menu_widget ! Destroying it".format(widgetName))
			if not self.widgetName[widgetName].isDestroyed:
				self.subWidgets[widgetName].destroy()
		realPos = self.getRealPos()
		self.subWidgets[widgetName] = widgetType(self.activity, (pos[0] + realPos[0], pos[1] + realPos[1]), *widgetArgs, **widgetKwargs)

	def removeSubWidget(self, widgetName):
		if widgetName in self.subWidgets:
			if not self.subWidgets[widgetName].isDestroyed:
				self.subWidgets[widgetName].destroy()
			self.subWidgets.pop(widgetName)
		else:
			print("[WARNING] [Menu_widget.removeSubWidget] No widget called \"{}\" in this Menu_widget".format(widgetName))

	def configSubWidget(self, widgetName, **kwargs):
		if widgetName in self.subWidgets:
			self.subWidgets[widgetName].config(**kwargs)
		else:
			print("[WARNING] [Menu_widget.configSubWidget] No widget called \"{}\" in this Menu_widget".format(widgetName))

	def update(self, deltaTime):
		if self.backgroundImage:
			self.activity.window.drawImage(self.backgroundImage, self.getRealPos())
		for widget in tuple(self.subWidgets.values()):
			if not widget.isDestroyed:
				widget.update(deltaTime)

	def onEvent(self, event):
		for widget in tuple(self.subWidgets.values()):
			if not widget.isDestroyed:
				widget.onEvent(event)

	def destroy(self):
		for widget in tuple(self.subWidgets.values()):
			if not widget.isDestroyed:
				widget.destroy()
		self.subWidgets.clear()
		self.activity.enableWidgets()
		Widget.destroy(self)

	def config(self, **kwargs):
		Widget.config(self, **kwargs)
		if "enable" in kwargs:
			for widget in self.subWidgets.values():
				widget.config(enable = kwargs["enable"])
