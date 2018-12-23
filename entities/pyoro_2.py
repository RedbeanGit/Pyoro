# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 18/03/2018
	@version: 1
=========================
"""

from entities.bean import Bean
from entities.leaf import Leaf
from entities.pyoro import Pyoro
from entities.seed import Seed
from game.config import PYORO_SHOOT_SPRITE_DURATION

class Pyoro_2(Pyoro):
	def __init__(self, level):
		self.shootSpriteId = 0
		Pyoro.__init__(self, level)

	def initImages(self):
		self.__initImages__("pyoro 2")

	def initSounds(self):
		self.__initSounds__(("pyoro_shoot",))
		Pyoro.initSounds(self)

	def enableMoveLeft(self):
		if self.shootSpriteId:
			self.shootSpriteId = 0
			self.level.removeActionDelay((self, "updateShootSpriteId"))
		Pyoro.enableMoveLeft(self)

	def enableMoveRight(self):
		if self.shootSpriteId:
			self.shootSpriteId = 0
			self.level.removeActionDelay((self, "updateShootSpriteId"))
		Pyoro.enableMoveRight(self)

	def update(self, deltaTime):
		if self.shootSpriteId == 1:
			self.level.createActionDelay((self, "updateShootSpriteId"), PYORO_SHOOT_SPRITE_DURATION, self.updateShootSpriteId)
		Pyoro.update(self, deltaTime)

	def updateShootSpriteId(self):
		self.shootSpriteId += 1
		if self.shootSpriteId < 5:
			self.level.setActionDelay((self, "updateShootSpriteId"), PYORO_SHOOT_SPRITE_DURATION, self.updateShootSpriteId)
		else:
			self.shootSpriteId = 0
			self.level.removeActionDelay((self, "updateShootSpriteId"))

	def updateSprite(self):
		styleType = self.level.getStyleTypeWithScore()
		if self.dead:
			self.currentImageName = "pyoro_{}_die_{}.png".format(styleType, self.direction)
		elif self.shootSpriteId:
			self.currentImageName = "pyoro_{}_shoot_{}_{}.png".format(styleType, self.shootSpriteId - 1, self.direction)
		elif self.notch:
			self.currentImageName = "pyoro_{}_jump_{}.png".format(styleType, self.direction)
		else:
			self.currentImageName = "pyoro_{}_normal_{}.png".format(styleType, self.direction)

	def enableCapacity(self):
		self.sounds["pyoro_shoot"].play()
		self.shootSpriteId = 1
		beanCoords = []
		for entity in self.level.entities:
			if self.isShootingEntity(entity):
				if isinstance(entity, Bean):
					entity.cut(); entity.catch(); entity.remove()
					beanCoords.append(list(entity.pos))
				elif isinstance(entity, Leaf):
					entity.cut()
					if self.direction == 1:
						entity.setRightWind()
					else:
						entity.setLeftWind()
		if len(beanCoords) == 1:
			score = 50
		elif len(beanCoords) == 2:
			score = 100
		elif len(beanCoords) == 3:
			score = 300
		else:
			score = 1000
		for beanPos in beanCoords:
			self.level.spawnScore(score, beanPos)
		self.level.entities.append(Seed(self.level, 35, self.direction))
		self.level.entities.append(Seed(self.level, 55, self.direction))

	def isShootingEntity(self, entity):
		if self.direction == 1:
			distance = entity.pos[0] - self.pos[0]
		else:
			distance = self.pos[0] - entity.pos[0]
		return (self.pos[1] - entity.pos[1] + entity.size[1] >= distance - entity.size[0]) \
			and (self.pos[1] - entity.pos[1] - entity.size[1] <= distance + entity.size[0])

	def disableCapacity(self):
		pass

	def remove(self):
		self.level.removeActionDelay((self, "updateShootSpriteId"))
		Pyoro.remove(self)