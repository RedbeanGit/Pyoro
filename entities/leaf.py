# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 07/05/2018
	@version: 1.1
=========================
"""

import random

from game.config import LEAF_SPEED, LEAF_SPRITE_DURATION, LEAF_WIND_SPEED, AIR_RESISTANCE
from entities.entity import Entity

class Leaf(Entity):
	def __init__(self, level, pos, speed, leafType):
		self.vel = 0
		self.spriteIndex = 0
		self.leafType = leafType
		self.speed = speed
		Entity.__init__(self, level, pos, (0.75, 0.75))

	def initImages(self):
		self.__initImages__(self.leafType)
	
	def update(self, deltaTime):
		self.pos[0] += self.vel * deltaTime
		self.pos[1] += (LEAF_SPEED - abs(self.vel)) * self.speed * deltaTime
		if self.vel > 0:
			self.vel -= AIR_RESISTANCE * deltaTime
			if self.vel < 0:
				self.vel = 0
		elif self.vel < 0:
			self.vel += AIR_RESISTANCE * deltaTime
			if self.vel > 0:
				self.vel = 0
		Entity.update(self, deltaTime)

	def updateSprite(self):
		self.spriteIndex = self.spriteIndex + 1 if self.spriteIndex < 2 else 0
		self.currentImageName = "leaf_{}_{}.png".format(self.level.getStyleTypeWithScore(), self.spriteIndex)
		self.level.setActionDelay((self, "updateSprite"), LEAF_SPRITE_DURATION, self.updateSprite)
	
	def setLeftWind(self):
		self.vel = -LEAF_WIND_SPEED
	
	def setRightWind(self):
		self.vel = LEAF_WIND_SPEED
	
	def cut(self):
		if not random.randint(0, 2):
			for deltaPos in (-self.size[0], self.size[0]):
				self.level.spawnLeafPiece((self.pos[0] + deltaPos / 2, self.pos[1]), self.speed, self.leafType + " piece", self.vel / 2)
			self.remove()
	
	def remove(self):
		self.level.removeActionDelay((self, "updateSprite"))
		Entity.remove(self)