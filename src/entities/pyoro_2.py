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
Provide a Pyoro class, the main character of the game.

Created on 18/03/2018.
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.bean import Bean
from entities.leaf import Leaf
from entities.pyoro import Pyoro
from entities.seed import Seed
from game.config import PYORO_SHOOT_SPRITE_DURATION


class Pyoro_2(Pyoro):
	"""
	Create a Pyoro 2 (a little yellow bird) controlled by the player in game.
	"""

	def __init__(self, level):
		"""
		Initialize a new Pyoro 2 object.

		:type level: game.level.Level
		:param level: The level managing this entity.
		"""

		self.shootSpriteId = 0
		Pyoro.__init__(self, level)

	def initImages(self):
		"""
		Initialize Pyoro 2 images.
		"""

		self.__initImages__("pyoro 2")

	def initSounds(self):
		"""
		Load Pyoro 2 sounds.
		"""

		self.__initSounds__(("pyoro_shoot",))
		Pyoro.initSounds(self)

	def enableMoveLeft(self):
		"""
		Make Pyoro 2 move to the left by defining its direction.
		"""

		if self.shootSpriteId:
			self.shootSpriteId = 0
			self.level.removeActionDelay((self, "updateShootSpriteId"))
		Pyoro.enableMoveLeft(self)

	def enableMoveRight(self):
		"""
		Make Pyoro 2 move to the right by defining its direction.
		"""

		if self.shootSpriteId:
			self.shootSpriteId = 0
			self.level.removeActionDelay((self, "updateShootSpriteId"))
		Pyoro.enableMoveRight(self)

	def update(self, deltaTime):
		"""
		Update Pyoro 2 (position, posture and sprite).

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last update.
		"""

		if self.shootSpriteId == 1:
			self.level.createActionDelay((self, "updateShootSpriteId"), \
				PYORO_SHOOT_SPRITE_DURATION, self.updateShootSpriteId)
		Pyoro.update(self, deltaTime)

	def updateShootSpriteId(self):
		"""
		Update shoot sprite index value for shoot animations.
		"""

		self.shootSpriteId += 1
		if self.shootSpriteId < 5:
			self.level.setActionDelay((self, "updateShootSpriteId"), \
				PYORO_SHOOT_SPRITE_DURATION, self.updateShootSpriteId)
		else:
			self.shootSpriteId = 0
			self.level.removeActionDelay((self, "updateShootSpriteId"))

	def updateSprite(self):
		"""
		Define the sprite to use (normal, shooting, jumping, dying)
		"""

		styleType = self.level.getStyleTypeWithScore()
		if self.dead:
			self.currentImageName = "pyoro_{}_die_{}.png".format(styleType, \
				self.direction)
		elif self.shootSpriteId:
			self.currentImageName = "pyoro_{}_shoot_{}_{}.png".format(styleType, \
				self.shootSpriteId - 1, self.direction)
		elif self.notch:
			self.currentImageName = "pyoro_{}_jump_{}.png".format(styleType, \
				self.direction)
		else:
			self.currentImageName = "pyoro_{}_normal_{}.png".format(styleType, \
				self.direction)

	def enableCapacity(self):
		"""
		Stop Pyoro 2 and make him cut some beans and leafs.
		"""

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
		"""
		Return True if entity is on the trajectory of a potential shot.

		:rtype: bool
		:returns: True if Pyoro 2 can shoot the entity, False otherwise.
		"""
		
		if self.direction == 1:
			distance = entity.pos[0] - self.pos[0]
		else:
			distance = self.pos[0] - entity.pos[0]
		return (self.pos[1] - entity.pos[1] + entity.size[1] >= distance - entity.size[0]) \
			and (self.pos[1] - entity.pos[1] - entity.size[1] <= distance + entity.size[0])

	def disableCapacity(self):
		"""
		Pyoro 2 doesn"t need this method so do nothing.
		"""
		pass

	def remove(self):
		"""
		Kill Pyoro 2 and remove its action delayed.
		"""

		self.level.removeActionDelay((self, "updateShootSpriteId"))
		Pyoro.remove(self)
