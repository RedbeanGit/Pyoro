# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 21/03/2018
	@version: 1
=========================
"""

from entities.entity import Entity
from game.config import SCORE_TEXT_BLINK_DURATION, SCORE_TEXT_LIFE_DURATION

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
		self.__initImages__("score text")
	
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