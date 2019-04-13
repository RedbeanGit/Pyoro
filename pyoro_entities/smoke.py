# -*- coding: utf-8 -*-

"""
Provide a class to create smoke animations

Created on 27/03/2018
"""

from pyoro_entities.entity import Entity
from pyoro_core.constants import SMOKE_SPRITE_DURATION

__author__ = "Julien Dubois"
__version__ = "2.0.0"


class Smoke(Entity):
	def __init__(self, level, pos):
		self.spriteIndex = 0
		Entity.__init__(self, level, pos, (1.5, 1.5))

	def initImages(self):
		imageNames = []
		for i in range(3):
			for j in range(3):
				imageNames.append("smoke_%s_%s.png" % (i, j))
		self.__initImages__("smoke", imageNames)

	def update(self, deltaTime):
		self.level.createActionDelay((self, "destroy"), SMOKE_SPRITE_DURATION * 3, self.remove)
		Entity.update(self, deltaTime)

	def updateSprite(self):
		self.spriteIndex = self.spriteIndex + 1 if self.spriteIndex < 2 else 0
		self.currentImageName = "smoke_{}_{}.png".format(self.level.getStyleTypeWithScore(), self.spriteIndex)
		self.level.setActionDelay((self, "updateSprite"), SMOKE_SPRITE_DURATION, self.updateSprite)

	def remove(self):
		self.level.removeActionDelay((self, "destroy"), (self, "updateSprite"))
		Entity.remove(self)
