# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 08/05/2018
	@version: 1
=========================
"""

from game.config import LEAF_SPRITE_DURATION
from entities.leaf import Leaf

class Leaf_piece(Leaf):
	def __init__(self, level, pos, speed, leafpieceType, vel = 0):
		Leaf.__init__(self, level, pos, speed, leafpieceType)
		self.vel = vel

	def initImages(self):
		self.__initImages__(self.leafType)

	def updateSprite(self):
		self.spriteIndex = self.spriteIndex + 1 if self.spriteIndex < 2 else 0
		self.currentImageName = "leafpiece_{}_{}.png".format(self.level.getStyleTypeWithScore(), self.spriteIndex)
		self.level.setActionDelay((self, "updateSprite"), LEAF_SPRITE_DURATION, self.updateSprite)

	def cut(self):
		pass