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
Provides a Bean class to represent falling beans
(as indicated by his name). Beans destroy blocks and kill Pyoro
if they touch it.

Created on 18/03/2018
"""

import random

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.entity import Entity
from game.config import BEAN_SPEED, BEAN_SPRITE_DURATION


class Bean(Entity):
	"""
	Main class for all falling beans
	"""

	def __init__(self, level, pos, speed):
		"""
		Initialize a Bean object.

		:type level: game.level.Level
		:param level: The level managing this bean.

		:type pos: list<float>
		:param pos: The default position of the bean.

		:type speed: float
		:param speed: The falling speed of the bean.
		"""

		self.caught = False
		self.speed = speed
		self.spriteIndex = 0
		Entity.__init__(self, level, pos, (1.5, 1.5))

	def initImages(self):
		"""
		Load bean images.
		"""

		self.__initImages__("bean")

	def initSounds(self):
		"""
		Load bean sounds.
		"""

		self.__initSounds__(("bean_cut", "bean_explode"))

	def update(self, deltaTime):
		"""
		Update the bean (position, sprite).

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last frame update
		"""

		if not self.caught:
			self.pos[1] += BEAN_SPEED * self.speed * deltaTime
			if self.isHittingTheFloor():
				if(self.level.cases[int(self.pos[0])].exists):
					self.level.cases[int(self.pos[0])].exists = False
					self.explode()
					self.remove()
			if(self.isHittingEntity(self.level.pyoro) \
			and not(self.level.pyoro.dead)):
				self.explode()
				self.remove()
				self.level.pyoro.remove()
		Entity.update(self, deltaTime)

	def updateSprite(self):
		"""
		Update the images to create a swing animation.
		"""

		self.spriteIndex = self.spriteIndex + 1 if self.spriteIndex < 2 else 0
		self.currentImageName = "bean_{}_{}.png".format( \
			self.level.getStyleTypeWithScore(), self.spriteIndex)
		
		self.level.setActionDelay((self, "updateSprite"), \
			BEAN_SPRITE_DURATION, self.updateSprite)

	def catch(self):
		"""
		Method called when caught by Pyoro.
		"""

		self.caught = True

	def explode(self):
		"""
		Create an explosion animation with smoke and by playing
		an explosion sound.
		"""

		self.sounds["bean_explode"].play()
		self.level.spawnSmoke(self.pos)

	def cut(self):
		"""
		Spawn leafs to create a cutting animation.
		"""

		self.sounds["bean_cut"].play()
		for i in range(2):
			randPos = [self.pos[0] + random.uniform(-0.5, 0.5), self.pos[1] \
				+ random.uniform(-0.5, 0.2)]
			self.level.spawnLeaf(randPos, "leaf")

	def remove(self):
		"""
		Remove the bean from its level and stop all actions delayed.
		"""

		self.level.removeActionDelay((self, "updateSprite"))
		Entity.remove(self)
