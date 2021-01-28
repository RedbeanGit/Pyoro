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
Provide a Seed class for Pyoro 2 shoot animation.

Created on 27/03/2018.
"""

import math
import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.entity import Entity
from gui.image_transformer import resizeImage
from game.config import SEED_SPEED, AIR_RESISTANCE, GRAVITY_FORCE, \
	ENTITIES_IMAGE_PATH


class Seed(Entity):
	"""
	Create seeds used for Pyoro 2 shoot animations.
	"""

	def __init__(self, level, angle, direction):
		"""
		Initialize a new Seed object.

		:type level: game.level.Level
		:param level: The level managing this object

		:type angle: float
		:param angle: The initial trajectory's angle in degree.

		:type direction: int
		:param direction: The direction of the seed (1=right, -1=left).
		"""

		self.direction = direction
		self.spriteAlpha = 255
		self.vel = [
			math.cos(angle * math.pi / 180) * direction * SEED_SPEED,
			-math.sin(angle * math.pi / 180) * SEED_SPEED
		]

		pos = (level.pyoro.pos[0] + (level.pyoro.size[0] / 2 + 0.0625) * direction,
			level.pyoro.pos[1] - level.pyoro.size[1] / 2 + 0.0625)

		Entity.__init__(self, level, pos, (0.125, 0.125))

	def __initImages__(self, folderName):
		"""
		Internally load seed images in memory.

		:type folderName: str
		:param folderName: The path to the folder containing the seeds.
		"""

		self.images = {}
		folder = os.path.join(ENTITIES_IMAGE_PATH, folderName)
		imageNames = os.listdir(folder)
		caseSize = self.level.levelDrawer.getCaseSize()

		for imageName in imageNames:
			if imageName.split(".")[-1] == "png":
				self.images[imageName] = resizeImage(
					self.level.levelDrawer.activity.window.getImage(
						os.path.join(folder, imageName),
						alphaChannel = False), \
					(caseSize[0] * self.size[0], caseSize[1] * self.size[1]))
				self.images[imageName].set_alpha(self.spriteAlpha)
				self.currentImageName = imageName

	def initImages(self):
		"""
		Initialize seed images.
		"""

		self.__initImages__("seed")

	def update(self, deltaTime):
		"""
		Update the seed (velocity, position, image opacity).

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last update.
		"""

		self.vel[0] -= AIR_RESISTANCE * self.direction * deltaTime
		self.vel[1] += GRAVITY_FORCE * deltaTime
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]

		if self.spriteAlpha > 0:
			self.spriteAlpha -= 64 * deltaTime
		else:
			self.remove()
		Entity.update(self, deltaTime)

	def updateSprite(self):
		"""
		Define the sprite to use according to the current level style
		"""

		self.currentImageName = "seed_{}.png".format( \
			self.level.getStyleTypeWithScore())
		self.images[self.currentImageName].set_alpha(self.spriteAlpha)
