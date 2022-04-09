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
Provides an Angel class.
This entity is used to repair destroyed cases

Created on 21/03/2018
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.entity import Entity
from game.config import ANGEL_SPEED, ANGEL_SPRITE_DURATION


class Angel(Entity):
	"""
	Angel that fall from the sky to repair a destroyed block
	"""

	def __init__(self, level, repairCase):
		"""
		Initialize an Angel object.

		:type level: game.level.Level
		:param level: The level managing this entity

		:type repairCase: game.case.Case
		:param repairCase: The block to repair
		"""

		self.spriteIndex = 0
		self.case = repairCase
		self.case.isRepairing = True
		Entity.__init__(self, level, (repairCase.pos + 0.75, 0.75), (1.5, 1.5))

	def initImages(self):
		"""
		Load angel images.
		"""

		self.__initImages__("angel")

	def initSounds(self):
		"""
		Load angel sounds and start playing a falling sound.
		"""

		self.__initSounds__(("angel_down",))
		self.sounds["angel_down"].play()
	
	def update(self, deltaTime):
		"""
		Update the angel (position, sprite).

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last frame update
		"""

		if self.case.isRepairing:
			self.pos[1] += ANGEL_SPEED * deltaTime
		else:
			self.pos[1] -= ANGEL_SPEED * deltaTime
		if self.isHittingTheFloor():
			self.repairCase()
		Entity.update(self, deltaTime)

	def repairCase(self, case = None):
		"""
		Repair a destroyed block.

		:type case: game.case.Case
		:param case: The block to repair.
			Leave None to repair the default block.
		"""

		case = case if case else self.case
		case.isRepairing = False
		case.exists = True
		self.sounds["angel_down"].stop()

	def updateSprite(self):
		"""
		Update the images to create a flight animation.
		"""

		self.spriteIndex = 1 if self.spriteIndex == 0 else 0
		self.currentImageName = "angel_{}_{}.png".format(self.level.getStyleTypeWithScore(), self.spriteIndex)
		self.level.setActionDelay((self, "updateSprite"), ANGEL_SPRITE_DURATION, self.updateSprite)
		
	def remove(self):
		"""
		Remove the angel from its level and stop all actions delayed.
		"""

		self.level.removeActionDelay((self, "updateSprite"))
		Entity.remove(self)