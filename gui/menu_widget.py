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
Provide a Menu_widget base class.

Created on 08/10/2018.
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH
from gui.image_transformer import stretchImage
from gui.widget import Widget


class Menu_widget(Widget):
	"""
	Create a widget used to pack subwidgets which will be updated by this
		menu.
	"""

	DEFAULT_KWARGS = {
		"backgroundImage": os.path.join(GUI_IMAGE_PATH, "frame.png")
	}

	def __init__(self, activity, pos, **kwargs):
		"""
		Initialize a new Menu objects.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The default position of the widget in a (x, y) tuple where
			x and y are integers.

		backgroundImage can be defined.
		"""

		Menu_widget.updateDefaultKwargs(kwargs)
		Widget.__init__(self, activity, pos, **kwargs)

		self.subWidgets = {}
		self.backgroundImage = None
		self.activity.disableWidgets()
		self.loadBackgroundImage()
		self.initWidgets()

	def loadBackgroundImage(self):
		"""
		Create the background from an image stretched to the widget size.
		"""
		
		if self.kwargs["backgroundImage"]:
			self.backgroundImage = stretchImage( \
				self.activity.window.getImage(self.kwargs["backgroundImage"]), \
				self.kwargs["size"], 5)

	def initWidgets(self):
		"""
		Initialize all subwidgets.
		"""

		pass

	def addSubWidget(self, widgetName, widgetType, pos, *widgetArgs, \
		**widgetKwargs):
		"""
		Create and add a new widget to this menu.

		:type widgetName: str
		:param widgetName: A string to identify the subwidget.

		:type widgetType: type
		:param widgetType: A type used to create the subwidget.

		:type pos: tuple
		:param pos: The default position of the subwidget relative to the
			upper left corner of the menu.

		Arguments and keyword arguments to pass to the subwidget can be
			defined then.
		"""

		if widgetName in self.subWidgets:
			print("[WARNING] [Menu_widget.addSubWidget] A widget " \
				+ "called \"{}\" already exists in".format(widgetName) \
				+ " this Menu_widget ! Destroying it")

			if not self.widgetName[widgetName].isDestroyed:
				self.subWidgets[widgetName].destroy()
		
		realPos = self.getRealPos()
		self.subWidgets[widgetName] = widgetType(self.activity, (pos[0] \
			+ realPos[0], pos[1] + realPos[1]), *widgetArgs, **widgetKwargs)

	def removeSubWidget(self, widgetName):
		"""
		Remove a subwidget from this menu.

		:type widgetName: str
		:param widgetName: The name used to identify the subwidget.
		"""

		if widgetName in self.subWidgets:
			if not self.subWidgets[widgetName].isDestroyed:
				self.subWidgets[widgetName].destroy()
			self.subWidgets.pop(widgetName)
		else:
			print("[WARNING] [Menu_widget.removeSubWidget] No widget called" \
				+ " \"{}\" in this Menu_widget".format(widgetName))

	def configSubWidget(self, widgetName, **kwargs):
		"""
		Call config method on a given subwidget.

		:type widgetName: str
		:param widgetName: The name used to identify the subwidget.

		Keyword arguments are passed to the subwidget.config method.
		"""

		if widgetName in self.subWidgets:
			self.subWidgets[widgetName].config(**kwargs)
		else:
			print("[WARNING] [Menu_widget.configSubWidget] No widget called" \
				+ " \"{}\" in this Menu_widget".format(widgetName))

	def update(self, deltaTime):
		"""
		Update the menu and its subwidgets.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last call of this method (in
			seconds).
		"""

		if self.backgroundImage:
			self.activity.window.drawImage(self.backgroundImage, \
				self.getRealPos())
		
		for widget in tuple(self.subWidgets.values()):
			if not widget.isDestroyed:
				widget.update(deltaTime)

	def onEvent(self, event):
		"""
		This method is called on all user events detected by Pygame.

		:type event: pygame.event.Event
		:param event: The event to handle.
		"""

		for widget in tuple(self.subWidgets.values()):
			if not widget.isDestroyed:
				widget.onEvent(event)

	def destroy(self):
		"""
		Destroy the menu and its subwidgets.
		"""

		for widget in tuple(self.subWidgets.values()):
			if not widget.isDestroyed:
				widget.destroy()
		self.subWidgets.clear()
		self.activity.enableWidgets()
		Widget.destroy(self)

	def config(self, **kwargs):
		"""
		Change some kwargs of the menu.
		"""

		Widget.config(self, **kwargs)
		if "enable" in kwargs:
			for widget in self.subWidgets.values():
				widget.config(enable = kwargs["enable"])
