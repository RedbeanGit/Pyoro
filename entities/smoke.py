# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 27/03/2018
	@version: 1
=========================
"""

from entities.entity import Entity
from game.config import SMOKE_SPRITE_DURATION

class Smoke(Entity):
	def __init__(self, level, pos):
		self.spriteIndex = 0
		Entity.__init__(self, level, pos, (1.5, 1.5))

	def initImages(self):
		self.__initImages__("smoke")
	
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