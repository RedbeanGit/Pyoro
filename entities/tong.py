# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 21/03/2018
	@version: 1
=========================
"""

from entities.bean import Bean
from entities.entity import Entity
from game.config import TONG_SPEED

class Tong(Entity):
	def __init__(self, level, direction):
		self.direction = direction
		self.caughtBean = None
		self.goBack = False

		pos = (level.pyoro.pos[0] + (level.pyoro.size[0] / 2 + 0.6) * direction,
			level.pyoro.pos[1] - level.pyoro.size[1] / 2 + 0.6)

		Entity.__init__(self, level, pos, (1.2, 1.2))

	def initImages(self):
		self.__initImages__("tong")

	def initSounds(self):
		self.__initSounds__(("tong", "pyoro_eat"))
		self.sounds["tong"].play()

	def update(self, deltaTime):
		w, h = self.level.size
		if self.goBack:
			self.pos[0] -= TONG_SPEED * 2 * self.direction * deltaTime
			self.pos[1] += TONG_SPEED * 2 * deltaTime

			if self.caughtBean:
				self.caughtBean.pos[0] -= TONG_SPEED * 2 * self.direction * deltaTime
				self.caughtBean.pos[1] += TONG_SPEED * 2 * deltaTime

			if self.pos[1] >= self.level.pyoro.pos[1]:
				if self.caughtBean:
					self.sounds["pyoro_eat"].play()
					self.level.pyoro.eatingCount = 1
				self.remove()
		else:
			self.pos[0] += TONG_SPEED * self.direction * deltaTime
			self.pos[1] -= TONG_SPEED * deltaTime

			for entity in self.level.entities:
				if self.isHittingEntity(entity) and isinstance(entity, Bean):
					entity.catch()
					self.sounds["tong"].stop()

					w, h = self.level.size
					if self.pos[1] < h * 0.2:
						score = 1000
					elif self.pos[1] < h * 0.4:
						score = 300
					elif self.pos[1] < h * 0.6:
						score = 100
					elif self.pos[1] < h * 0.8:
						score = 50
					else:
						score = 10
					self.level.spawnScore(score, self.pos)
					self.caughtBean = entity
					self.goBack = True
					return None
			self.goBack = self.isOutOfBounds(False)
		self.updateSprite()
		Entity.update(self, deltaTime)

	def updateSprite(self):
		self.currentImageName = "tong_{}_{}.png".format(self.level.getStyleTypeWithScore(), self.direction)

	def remove(self):
		if self.caughtBean:
			self.caughtBean.remove()
		self.level.pyoro.tong = None
		Entity.remove(self)
