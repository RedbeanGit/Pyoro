# -*- coding: utf-8 -*-

"""
Provide a class to manage widget dispositions, according to the screen
resolution.

Created on 16/12/2018
"""

from game.util import getLayoutTemplate

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

		w, h = self.window.getSize()
		self.width = width if width else w
		self.height = height if height else h
		self.template = getLayoutTemplate(self.width / self.height)

	def getWidgetPos(self, widgetName):
		"""
		Return the absolute position of a widget, in pixel.

		:type widgetName: str
		:param widgetName: A string representing a widget.

		:rtype: tuple
		:returns: (x, y) coordinates referencing the widget position.
			If something wrong happen, return (0, 0)
		"""

		if widgetName in self.template:
			winfos = self.template[widgetName]

			if "pos" in winfos:
				pos = winfos["pos"]
				if isinstance(pos, list):
					if len(pos) == 2:
						return int(pos[0] * self.width), \
							int(pos[1] * self.height) 
					
					print("[WARNING] [Layout.getWidgetPos] pos doesn't " \
						+ "seem to respect [x, y] template")
				else:
					print("[WARNING] [Layout.getWidgetPos] pos must be" \
						+ " a [x, y] list")
			else:
				print("[WARNING] [Layout.getWidgetPos] Pos not found for" \
					+ '"%s" widget' % widgetName)
		else:
			print("[WARNING] [Layout.getWidgetPos] No widget " \
				+ '"%s" found' % widgetName)
		
		return 0, 0

	def getWidgetSize(self, widgetName):
		"""
		Return the size of a widget, in pixel.

		:type widgetName: str
		:param widgetName: A string representing a widget.

		:rtype: tuple
		:returns: (w, h) tuple referencing the widget size.
			If something wrong happen, return (1, 1)
		"""

		if widgetName in self.template:
			winfos = self.template[widgetName]
			aspectRatio = self.getAspectRatio(widgetName)

			if "size" in winfos:
				size = winfos["size"]
				if isinstance(size, list):
					if len(size) == 2:
						
						if size[0] > 0 or size[1] > 0:
							if size[0] == -1:
								return int(size[1]*aspectRatio*self.height), \
									int(size[1] * self.height)
							elif size[1] == -1:
								return int(size[0] * self.width), \
									int(size[0] / aspectRatio * self.width)
							return int(size[0] * self.width), \
								int(size[1] * self.height)

						else:
							print("[WARNING] [Layout.getWidgetSize] Width " \
								+ "and/or height must be positive")
					else:
						print("[WARNING] [Layout.getWidgetSize] size " \
							+ "doesn't seem to respect [w, h] template")
				else:
					print("[WARNING] [Layout.getWidgetSize] size must be" \
						+ " a [w, h] list")
			else:
				print("[WARNING] [Layout.getWidgetSize] size not found for" \
					+ '"%s" widget' % widgetName)
		else:
			print("[WARNING] [Layout.getWidgetSize] No widget " \
				+ '"%s" found' % widgetName)

		return 1, 1

	def getAspectRatio(self, widgetName):
		"""
		Return the ratio of the width and height of a widget.

		:type widgetName: str
		:param widgetName: A string representing a widget.

		:rtype: float
		:returns: The ratio between the width and the height of the widget.
		"""

		if widgetName in self.template:
			winfos = self.template[widgetName]

			if "aspectRatio" in winfos:
				return winfos["aspectRatio"]
			else:
				print("[WARNING] [Layout.getAspectRatio] aspectRatio" \
					+ ' not found for "%s" widget' % widgetName)
		else:
			print("[WARNING] [Layout.getAspectRatio] No widget " \
				+ '"%s" found' % widgetName)
		return 1

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

		if widgetName in self.template:
			winfos = self.template[widgetName]

			if "anchor" in winfos:
				anchor = winfos["anchor"]
				if isinstance(anchor, list):
					if len(anchor) == 2:
						return tuple(anchor)

					print("[WARNING] [Layout.getWidgetAnchor] anchor " \
						+ "doesn't seem to respect [x, y] template")
				else:
					print("[WARNING] [Layout.getWidgetPosAnchor] pos must" \
						+ " be a [x, y] list")
			else:
				print("[WARNING] [Layout.getWidgetAnchor] anchor not found" \
					+ ' for "%s" widget' % widgetName)
		else:
			print("[WARNING] [Layout.getWidgetAnchor] No widget " \
				+ '"%s" found' % widgetName)
		
		return 0, 0