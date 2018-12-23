# -*- coding:utf-8 -*-

"""
Provide a base class for activities.

Created on 15/08/2018
"""

from game.util import Game
from gui.layout import Layout
from gui.widget import Widget

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import os


class Activity:
	""" Abstract class for all layouts """

	def __init__(self, window):
		"""
		Initialize a new Activity object.

		:type window: gui.window.Window
		:param window: The parent window which will manage this activity.
		"""

		self.window = window
		self.layout = Layout(window)
		self.widgetOrder = []
		self.widgets = {}
		self.images = {}
		self.sounds = {}

		self.layout.load()
		self.initImages()
		self.initSounds()
		self.initWidgets()

	def initImages(self):
		pass

	def __initSounds__(self, soundNames, folder, audioType = "sound"):
		if audioType == "sound":
			fct = Game.audioPlayer.getSound
		elif audioType == "music":
			fct = Game.audioPlayer.getMusic
		for name in soundNames:
			self.sounds[name] = fct(os.path.join(folder, "{}.wav".format(name)))

	def initSounds(self):
		pass

	def initWidgets(self):
		pass



	def getWidgets(self):
		for widgetName in self.widgetOrder:
			if widgetName in self.widgets:
				yield self.widgets[widgetName]

	def addWidget(self, widgetName, widgetType, *args, **kwargs):
		if widgetName in self.widgets:
			print("[WARNING] [Layout.addWidget] Widget \"{}\" already exists".format(widgetName))
		else:
			widget = widgetType(self, *args, **kwargs)
			self.widgetOrder.append(widgetName)
			self.widgets[widgetName] = widget

	def removeWidget(self, widgetName):
		if widgetName in self.widgets:
			if not self.widgets[widgetName].isDestroyed:
				self.widgets[widgetName].destroy()
			self.widgets.pop(widgetName)
			self.widgetOrder.remove(widgetName)
		else:
			print("[WARNING] [Layout.removeWidget] \"{}\" not in widget list".format(widgetName))



	def enableWidgets(self):
		for widget in self.getWidgets():
			widget.config(enable = True)

	def disableWidgets(self):
		for widget in self.getWidgets():
			widget.config(enable = False)



	def updateEvent(self, event):
		for widget in self.getWidgets():
			if not widget.isDestroyed:
				widget.onEvent(event)

	def update(self, deltaTime):
		for widget in self.getWidgets():
			if not widget.isDestroyed:
				widget.update(deltaTime)

	def destroy(self):
		for widget in self.getWidgets():
			if not widget.isDestroyed:
				widget.destroy()
		self.widgetOrder.clear()
		self.widgets.clear()
		Game.audioPlayer.stopAudio()