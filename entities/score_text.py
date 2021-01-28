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
Provide a Score_text class (entity).

Created on 21/03/2018.
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.entity import Entity
from game.config import SCORE_TEXT_BLINK_DURATION, SCORE_TEXT_LIFE_DURATION


class Score_text(Entity):
	"""
	Create a Score_text which is a flashy entity to show points that has just
		been earned at a specific position.
	"""

	def __init__(self, level, pos, value):
		"""
		Initialize a new Score_text object.

		:type level: game.level.Level
		:param level: The level managing this entity.

		:type pos: list
		:param pos: An [x, y] list where x and y are both float numbers.

		:type value: int
		:param value: The value to display (it can be 10, 50, 100, 300 or
			1000).
		"""

		pixelSize = 1
		for number in str(value):
			if value == 1:
				pixelSize += 2
			else:
				pixelSize += 4
		self.value = value
		self.colorIndex = 0
		Entity.__init__(self, level, pos, (pixelSize * 0.125, 0.875))

	def initImages(self):
		"""
		Initialize score_text images.
		"""

		self.__initImages__("score text")
	
	def update(self, deltaTime):
		"""
		Update the score_text.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last update.
		"""

		self.level.createActionDelay((self, "destroy"), SCORE_TEXT_LIFE_DURATION, self.remove)
		Entity.update(self, deltaTime)
	
	def updateSprite(self):
		"""
		Change the sprite to make a blinking effect.
		"""

		if self.value in (300, 1000):
			self.colorIndex = self.colorIndex + 1 if self.colorIndex < 5 else 0
			self.currentImageName = "number_{}_{}.png".format(self.value, self.colorIndex)
		else:
			self.currentImageName = "number_{}.png".format(self.value)
		self.level.setActionDelay((self, "updateSprite"), SCORE_TEXT_BLINK_DURATION, self.updateSprite)
	
	def remove(self):
		"""
		Remove the score_text actions delayed en the score_text itself.
		"""

		self.level.removeActionDelay((self, "destroy"), (self, "updateSprite"))
		Entity.remove(self)