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
Provide a Score_text class (entity).

Created on 17/03/2018.
"""

import random

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.bean import Bean
from game.config import BEAN_SPRITE_DURATION


class Super_bean(Bean):
	"""
	Create a Super_bean object which have the hability to repair 10 destroyed
		cases and to explode all beans currently falling.
	"""
	def __init__(self, level, pos, speed):
		"""
		Initialize a new Super_bean object.

		:type level: game.level.Level
		:param level: The level managing this entity.

		:type pos: list
		:param pos: An [x, y] list where x and y are both float numbers.

		:type speed: float
		:param speed: The falling speed multiplicator.
		"""

		self.spriteIndex = 0
		self.colorIndex = 0
		Bean.__init__(self, level, pos, speed)

	def initImages(self):
		"""
		Initialize super_bean images.
		"""

		self.__initImages__("super bean")

	def initSounds(self):
		"""
		Load super_bean sounds.
		"""

		Bean.initSounds(self)
		self.__initSounds__(("bean_implode",))

	def updateSprite(self):
		"""
		Define the sprite to use according to the blinking animation state and
			the current level style.
		"""

		if not self.colorIndex % 2:
			self.spriteIndex = self.spriteIndex + 1 if self.spriteIndex < 2 else 0

		self.colorIndex = self.colorIndex + 1 if self.colorIndex < 5 else 0
		self.currentImageName = "bean_{}_{}.png".format(self.spriteIndex, \
			self.colorIndex)
		
		self.level.setActionDelay((self, "updateSprite"), \
			BEAN_SPRITE_DURATION / 6, self.updateSprite)

	def catch(self):
		"""
		Explode all the beans currently falling and repair 10 destroyed cases.
		"""

		i = 0
		for entity in self.level.entities:
			if isinstance(entity, Bean) and entity != self:
				self.level.createActionDelay((self, "destroyBean", i), i * 0.1, \
					self.destroyBean, entity, i)
				i += 1
		i = 0
		emptyCases = list(self.level.getVoidCases())
		for i in range(min(10, len(emptyCases))):
			self.level.createActionDelay((self, "repairCase", emptyCases[i].pos), \
				i * 0.5, self.repairCase, emptyCases[i])
		Bean.catch(self)

	def destroyBean(self, bean, beanId):
		"""
		Explode a bean, increase the score and remove action delayed
			associated with this bean.

		:type bean: entities.bean.Bean
		:param bean: The bean to destroy.

		:type beanId: int
		:param beanId: An integer associated with this bean when the explosion
			was decided.
		"""

		self.sounds["bean_implode"].play()
		bean.cut()
		bean.remove()
		self.level.spawnScore(50, bean.pos)
		self.level.removeActionDelay((self, "destroyBean", beanId))

	def cut(self):
		"""
		Spawn super leafs and play a sound.
		"""

		self.sounds["bean_cut"].play()
		for i in range(2):
			randPos = [self.pos[0] + random.uniform(-0.5, 0.5), \
				self.pos[1] + random.uniform(-0.5, 0.2)]
			self.level.spawnLeaf(randPos, "super leaf")

	def repairCase(self, case):
		"""
		Repair a case and remove the associated action delayed.

		:type case: game.case.Case
		:param case: The case to repair.
		"""

		self.level.repairCase(case)
		self.level.removeActionDelay((self, "repairCase", case.pos))

	def remove(self):
		"""
		Remove the super bean action delayed and the super bean itself.
		"""
		
		self.level.removeActionDelay(("override", self, "updateSprite"))
		Bean.remove(self)
