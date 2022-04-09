# -*- coding: utf-8 -*-

#   This file is part of Pyoro (A Python fan game).
#
#   Metawars is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Metawars is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
Provide a Widget abstract base class for all ui components.

Created in 28/03/2018.
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"


class Widget:
	"""
	Create abstract Widget objects. A widget is a User Interface component
		(like buttons, texts, title images, ...). All widgets have default
		parameters defined in Widget.DEFAULT_KWARGS (replace Widget by the
		widget class you want to get the default keyword arguments handled).
	"""

	DEFAULT_KWARGS = {
		"size": [1, 1],
		"anchor": (-1, -1)
	}

	def __init__(self, activity, pos, **kwargs):
		"""
		Initialize a new Widget object.

		:type activity: gui.activity.Activity
		:param activity: The parent activity managing the widget.

		:type pos: tuple
		:param pos: A (x, y) tuple where x and y are both integers.

		A size (list) and an anchor (tuple) argument can also be passed to
			this method.
		"""

		Widget.updateDefaultKwargs(kwargs)
		self.activity = activity
		self.pos = pos
		self.isDestroyed = False
		self.kwargs = dict(kwargs)

	@classmethod
	def updateDefaultKwargs(cls, kwargs):
		"""
		Add missing optional kwargs with Widget.DEFAULT_KWARGS.

		:type kwargs: dict
		:param kwargs: A {kwargsName: value} dictionnary to update with
			missing kwargs.
		"""

		for key, value in cls.DEFAULT_KWARGS.items():
			if key not in kwargs:
				kwargs[key] = value

	def update(self, deltaTime):
		"""
		Update the widget.
		Do nothing by default. This method has to be overridden.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last call of this method (in
			seconds).
		"""
		pass

	def onEvent(self, event):
		"""
		This method is called to handled each user events detected by pygame.
		Do nothing by default. This method has to be overridden.

		:type event: pygame.event.Event
		:param event: A pygame event.
		"""
		pass

	def config(self, **kwargs):
		"""
		Change some kwargs of the widget.
		"""
		
		for key, value in kwargs.items():
			self.kwargs[key] = value

	def getRealPos(self):
		"""
		Return the (x, y) position in pixel of the top left corner of the
			widget.

		:rtype: list
		:returns: A [x, y] list where x and y are both integers.
		"""

		x = int(self.pos[0] - self.kwargs["size"][0] \
			* (self.kwargs["anchor"][0] + 1) / 2)
		y = int(self.pos[1] - self.kwargs["size"][1] \
			* (self.kwargs["anchor"][1] + 1) / 2)

		return [x, y]

	def isInWidget(self, pos):
		"""
		Check if a given (x, y) position is within the widget box.

		:type pos: tuple
		:param pos: A (x, y) position to check where x and y are both float
			numbers.

		:rtype: bool
		:returns: True if the position is in the widget box. False otherwise.
		"""

		realPos = self.getRealPos()
		
		return pos[0] >= realPos[0] \
		   and pos[0] <= realPos[0] + self.kwargs["size"][0] \
		   and pos[1] >= realPos[1] \
		   and pos[1] <= realPos[1] + self.kwargs["size"][1]

	def destroy(self):
		"""
		Destroy the widget.
		"""

		self.isDestroyed = True
