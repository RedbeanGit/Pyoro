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
Provide a base class for activities.

Created on 15/08/2018
"""

import collections
import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.util import Game
from gui.layout import Layout
from gui.widget import Widget


class Activity:
	"""
	Abstract class for all activities.
	"""

	def __init__(self, window):
		"""
		Initialize a new Activity object.

		:type window: gui.window.Window
		:param window: The parent window which will manage this activity.
		"""

		self.window = window
		self.layout = Layout(window)
		self.widgets = collections.OrderedDict()
		self.sounds = {}

		self.layout.load()
		self.initSounds()
		self.initWidgets()

	def __initSounds__(self, soundNames, folder, audioType = "sound"):
		"""
		Useful method to easily load sounds or musics which will be used later
		by this activity. Do not override this method.

		:type soundNames: tuple
		:param soundNames: Base filename of the sounds to load.

		:type folder: str
		:param folder: The filepath of the folder where sounds are located.

		:type audioType: str
		:param audioType: (Optional) How to load the sound (as sound or as music).
			Default is "sound". It can be "sound" or "music".
		"""

		if audioType == "sound":
			fct = Game.audioPlayer.getSound
		elif audioType == "music":
			fct = Game.audioPlayer.getMusic
		for name in soundNames:
			self.sounds[name] = fct(os.path.join(folder, "{}.wav".format(name)))

	def initSounds(self):
		"""
		This method should be override. It's called when the activity is
		initialized. It's used to load the sounds used by this activity.
		"""
		pass

	def initWidgets(self):
		"""
		This method should be override. It's called when the activity is
		initialized. It's used to load the widgets used by this activity.
		"""
		pass

	def addWidget(self, widgetName, widgetType, *args, **kwargs):
		"""
		Add a widget with a defined name and arguments.

		:type widgetName: str
		:param widgetName: The name of the widget. This name can be use later to
			get or remove the widget.

		:type widgetType: class
		:param widgetType: The class of the widget to add. This class is used to
			create the widget.
		"""

		if widgetName in self.widgets:
			print("[WARNING] [Layout.addWidget] Widget '%s' already exists" % widgetName)
		else:
			widget = widgetType(self, *args, **kwargs)
			self.widgets[widgetName] = widget

	def removeWidget(self, widgetName):
		"""
		Remove a widget from this activity.

		:type widgetName: str
		:param widgetName: The name of the widget to destroy and remove.
		"""

		if widgetName in self.widgets:
			if not self.widgets[widgetName].isDestroyed:
				self.widgets[widgetName].destroy()
			self.widgets.pop(widgetName)
		else:
			print("[WARNING] [Layout.removeWidget] '%s' not in widget list" % widgetName)

	def enableWidgets(self):
		"""
		Enable all widgets of this activity.
		"""

		for widget in tuple(self.widgets.values()):
			widget.config(enable = True)

	def disableWidgets(self):
		"""
		Disable all widgets of this activity.
		"""

		for widget in tuple(self.widgets.values()):
			widget.config(enable = False)

	def updateEvent(self, event):
		"""
		Update all widgets of this activity by giving to them a defined pygame
		event.

		:type event: pygame.event.Event
		:param event: The event to pass to the widgets.
		"""

		for widget in tuple(self.widgets.values()):
			if not widget.isDestroyed:
				widget.onEvent(event)

	def update(self, deltaTime):
		"""
		Update all graphical components of this activity.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last call of this method (in
			seconds).
		"""

		for widget in tuple(self.widgets.values()):
			if not widget.isDestroyed:
				widget.update(deltaTime)

	def destroy(self):
		"""
		Destroy all widgets of this activity.
		"""

		for widget in tuple(self.widgets.values()):
			if not widget.isDestroyed:
				widget.destroy()
		self.widgets.clear()
