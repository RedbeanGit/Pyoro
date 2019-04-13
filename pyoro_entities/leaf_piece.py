# -*- coding: utf-8 -*-

"""
Provides a class to create cut leafs.

Created on 08/05/2018
"""

from pyoro_core.constants import LEAF_SPRITE_DURATION
from pyoro_entities.leaf import Leaf


class Leaf_piece(Leaf):
	def __init__(self, level, pos, speed, leafpieceType, vel = 0):
		Leaf.__init__(self, level, pos, speed, leafpieceType)
		self.vel = vel

	def initImages(self):
		imageNames = []
		for i in range(3):
			for j in range(3):
				imageNames.append("leafpiece_%s_%s.png" % (i, j))
		self.__initImages__(self.leafType, imageNames)

	def updateSprite(self):
		self.spriteIndex = self.spriteIndex + 1 if self.spriteIndex < 2 else 0
		self.currentImageName = "leafpiece_{}_{}.png".format(self.level.getStyleTypeWithScore(), self.spriteIndex)
		self.level.setActionDelay((self, "updateSprite"), LEAF_SPRITE_DURATION, self.updateSprite)

	def cut(self):
		pass
