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
Provide a Tongue class.

Created on 21/03/2018.
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.bean import Bean
from entities.entity import Entity
from game.config import TONG_SPEED


class Tongue(Entity):
	"""
	Creat a Tongue object used by Pyoro to catch falling beans.
	"""

	def __init__(self, level, direction):
		"""
		Initialize a new Tongue object.

		:type level: game.level.Level
		:param level: The level managing this entity.

		:type direction: int
		:param direction: The direction of the tongue (1 = right, -1 = left).
		"""

		self.direction = direction
		self.caughtBean = None
		self.goBack = False

		pos = (level.pyoro.pos[0] + (level.pyoro.size[0] / 2 + 0.6) * direction,
			level.pyoro.pos[1] - level.pyoro.size[1] / 2 + 0.6)

		Entity.__init__(self, level, pos, (1.2, 1.2))

	def initImages(self):
		"""
		Initialize tongue images.
		"""

		self.__initImages__("tongue")

	def initSounds(self):
		"""
		Load tongue sounds.
		"""

		self.__initSounds__(("tongue", "pyoro_eat"))
		self.sounds["tongue"].play()

	def update(self, deltaTime):
		"""
		Update the tongue (position, direction, ...).

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last update.
		"""

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
					self.sounds["tongue"].stop()

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
		"""
		Define the sprite to use according to the current level style.
		"""

		self.currentImageName = "tongue_{}_{}.png".format( \
			self.level.getStyleTypeWithScore(), self.direction)

	def remove(self):
		"""
		Remove the caught bean and the tongue itself.
		"""

		if self.caughtBean:
			self.caughtBean.remove()
		self.level.pyoro.tongue = None
		Entity.remove(self)
