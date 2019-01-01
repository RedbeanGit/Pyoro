# -*- coding: utf-8 -*-

"""
Provide a class to manage widget dispositions, according to the screen
resolution.

Created on 16/12/2018
"""

from game.util import getLayoutTemplate, getScreenRatio, getScreenSize, \
	getMonitorSize

__author__ = "Julien Dubois"
__version__ = "1.1.2"


class Layout:
	"""
	Layout help to get widgets size, position and anchor according to
	the window resolution.
	"""

	def __init__(self, window):
		"""
		Initialize a ne Layout object.

		:type window: gui.window.Window
		:param window: A game window to work with.
		"""

		self.window = window
		self.width = 1
		self.height = 1
		self.width_mm = 1
		self.height_mm = 1
		self.dpm = 1
		self.template = {}

	def load(self, width = None, height = None):
		"""
		Try to load a layout template adapted to a defined resolution.

		:type width: int
		:param width: (Optional) The width of the window (in pixel). Leave
			None to use	the current window width.

		:type height: int
		:param height: (Optional) The height of the window (in pixel). Leave
			None to use the current window height.
		"""

		self.width, self.height = getScreenSize()
		self.width_mm, self.height_mm = getMonitorSize()
		self.dpm = (self.width / self.width_mm \
			+ self.height / self.height_mm) / 2
		self.template = getLayoutTemplate(getScreenRatio())

	def getWidgetPos(self, widgetName):
		"""
		Return the absolute position of a widget, in pixel.

		:type widgetName: str
		:param widgetName: A string representing a widget.

		:rtype: tuple
		:returns: (x, y) coordinates referencing the widget position.
			If something wrong happen, return (0, 0)
		"""

		w, h = self.getWidgetInfo(widgetName, "pos", [0, 0])
		return int(w * self.width / 100), int(h * self.height / 100)

	def getWidgetSize(self, widgetName):
		"""
		Return the size of a widget, in pixel.

		:type widgetName: str
		:param widgetName: A string representing a widget.

		:rtype: tuple
		:returns: (w, h) tuple referencing the widget size.
		"""

		mw, mh = self.getWidgetInfo(widgetName, "min_mm_format", [0, 0])
		wm, hm = self.getWidgetInfo(widgetName, "size_mm", [1, 1])
		wp, hp = self.getWidgetInfo(widgetName, "size", [1, 1])
		w, h = wp * self.width / 100, hp * self.height / 100

		if self.width_mm >= mw:
			w = wm * self.dpm

		if self.height_mm >= mh:
			h = hm * self.dpm

		return int(w), int(h)

	def getWidgetAnchor(self, widgetName):
		"""
		Return the anchor position of a widget.

		:type widgetName: str
		:param widgetName: A string representing a widget.

		:rtype: tuple
		:returns: (x, y) coordinates referencing the widget anchor point,
			relative to the widget position. If something wrong happen,
			return (0, 0).
		"""

		return self.getWidgetInfo(widgetName, "anchor", [0, 0])

	def getFontSize(self, widgetName):
		"""
		Return the font size of a text widget.

		:type widgetName: str
		:param widgetName: A string representing a text widget.

		:rtype: int
		:returns: The font size in pixel.
		"""

		mw, mh = self.getWidgetInfo(widgetName, "min_mm_format", [0, 0])
		sm = self.getWidgetInfo(widgetName, "font_size_mm", 1)
		sp = self.getWidgetInfo(widgetName, "font_size", 1)

		if self.height_mm < mh or self.width_mm < mw:
			return int(sp * (self.height + self.width) / 200)
		return int(sm * self.dpm)

	def getWidgetInfo(self, widgetName, info, defaultValue = None):
		"""
		Return an information for a given widget.

		:type widgetName: str
		:param widgetName: A string representing a widget.

		:type info: str
		:param info: The name of info searched.

		:type defaultValue: object
		:param defaultValue: (Optional). The returned value if something wrong
			happen.

		:Example: layout.getWidgetInfo("play_button_1", "size", [1, 1])
		"""

		if widgetName in self.template:
			if info in self.template[widgetName]:
				return self.template[widgetName][info]
			print('[WARNING] [Layout.getWidgetInfo] No info ' \
				+ '"%s" for "%s"' % (info, widgetName))
		else:
			print('[WARNING] [Layout.getWidgetInfo] No widget "%s" found' % widgetName)
		return defaultValue
