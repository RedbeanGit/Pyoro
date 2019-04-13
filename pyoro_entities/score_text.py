# -*- coding: utf-8 -*-

"""
Provide a class to create text (only some numbers) as an entity

Created on 21/03/2018
"""

from pyoro_entities.entity import Entity
from pyoro_core.constants import SCORE_TEXT_BLINK_DURATION, SCORE_TEXT_LIFE_DURATION

__author__ = "Julien Dubois"
__verison__ = "2.0.0"


class Score_text(Entity):
	def __init__(self, level, pos, value):
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
		imageNames = []
		for i in (10, 50, 100):
			imageNames.append("number_%s.png" % i)
		for i in (300, 1000):
			for j in range(6):
				imageNames.append("number_%s_%s.png" % (i, j))
		self.__initImages__("score text", imageNames)

	def update(self, deltaTime):
		self.level.createActionDelay((self, "destroy"), SCORE_TEXT_LIFE_DURATION, self.remove)
		Entity.update(self, deltaTime)

	def updateSprite(self):
		if self.value in (300, 1000):
			self.colorIndex = self.colorIndex + 1 if self.colorIndex < 5 else 0
			self.currentImageName = "number_{}_{}.png".format(self.value, self.colorIndex)
		else:
			self.currentImageName = "number_{}.png".format(self.value)
		self.level.setActionDelay((self, "updateSprite"), SCORE_TEXT_BLINK_DURATION, self.updateSprite)

	def remove(self):
		self.level.removeActionDelay((self, "destroy"), (self, "updateSprite"))
		Entity.remove(self)
