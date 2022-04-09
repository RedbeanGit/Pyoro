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

from entities.entity import Entity
from entities.tongue import Tongue
from game.config import PYORO_SPEED, PYORO_NOTCH_DURATION,  \
	PYORO_EATING_DURATION, PYORO_DIE_SPEED


class Pyoro(Entity):
	"""
	Create a Pyoro (a little red bird) controlled by the player in game.
	"""

	def __init__(self, level):
		"""
		Initialize a new Pyoro object.

		:type level: game.level.Level
		:param level: The level managing this entity.
		"""

		self.moving = False
		self.notch = False
		self.dead = False
		self.tongue = None
		self.eatingCount = 0
		self.direction = 1
		w, h = level.size
		Entity.__init__(self, level, (2, h - 2), (2, 2))

	def initImages(self):
		"""
		Initialize Pyoro images.
		"""

		self.__initImages__("pyoro 1")

	def initSounds(self):
		"""
		Load Pyoro sounds.
		"""

		self.__initSounds__(("pyoro_move", "pyoro_die"))

	# directions
	def enableMoveRight(self):
		"""
		Make Pyoro move to the right by defining its direction.
		"""

		if not(self.dead) and not(self.tongue):
			self.direction = 1
			self.moving = True
			self.sounds["pyoro_move"].play(-1)

	def enableMoveLeft(self):
		"""
		Make Pyoro move to the left by defining its direction.
		"""

		if not(self.dead) and not(self.tongue):
			self.direction = -1
			self.moving = True
			self.sounds["pyoro_move"].play(-1)

	def disableMove(self):
		"""
		Stop Pyoro movement.
		"""

		if self.sounds["pyoro_move"].isPlaying:
			self.sounds["pyoro_move"].pause()
		self.moving = False
		self.notch = False

	def move(self, deltaTime):
		"""
		Update Pyoro's position according to elapsed time.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last update.
		"""

		if not(self.dead) and not(self.tongue):
			if not self.notch:
				if self.direction == 1:
					newPos = self.pos[0] + self.size[0] / 2 + PYORO_SPEED \
						* deltaTime
					voidPos = self.getVoidCasePosOnPath(newPos)

					if newPos >= self.level.size[0]:
						self.pos[0] = self.level.size[0] - self.size[0] / 2
					elif voidPos != None:
						self.pos[0] = voidPos - self.size[0] / 2
					else:
						self.pos[0] += PYORO_SPEED * deltaTime

				else:
					newPos = self.pos[0] - self.size[0] / 2 - PYORO_SPEED \
						* deltaTime
					voidPos = self.getVoidCasePosOnPath(newPos)
					if newPos < 0:
						self.pos[0] = self.size[0] / 2
					elif voidPos != None:
						self.pos[0] = voidPos + self.size[0] / 2 + 1
					else:
						self.pos[0] -= PYORO_SPEED * deltaTime
				self.level.createActionDelay((self, "enableNotch"), \
					PYORO_NOTCH_DURATION, self.enableNotch)

	def getVoidCasePosOnPath(self, newPos):
		"""
		Find the nearest hole from Pyoro. If there is no hole, return None.

		:type newPos: float
		:param newPos: The horizontal position where Pyoro try to go.

		:rtype: int, None
		:returns: The nearest destroyed case index (or none if there is no
			destroyed case).
		"""

		if self.pos[0] < newPos:
			oldPos = int(self.pos[0] + self.size[0] / 2)
			newPos = min(int(newPos), len(self.level.cases) - 1)
			for i in range(oldPos, newPos + 1):
				if not self.level.cases[i].exists:
					return i
		else:
			oldPos = int(self.pos[0] - self.size[0] / 2 - 1)
			newPos = max(int(newPos), 0)
			for i in range(oldPos, newPos - 1, -1):
				if not self.level.cases[i].exists:
					return i
		return None

	def enableNotch(self):
		"""
		Make Pyoro do a little jump.
		"""

		self.notch = True
		self.level.removeActionDelay((self, "enableNotch"))
		self.level.createActionDelay((self, "disableNotch"), \
			PYORO_NOTCH_DURATION, self.disableNotch)

	def disableNotch(self):
		"""
		Make Pyoro return to normal posture.
		"""

		self.notch = False
		self.level.removeActionDelay((self, "disableNotch"))

	# update method
	def update(self, deltaTime):
		"""
		Update Pyoro (position, posture and sprite).

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last update.
		"""

		if self.moving:
			self.move(deltaTime)
		else:
			self.level.removeActionDelay((self, "enableNotch"))
			self.disableNotch()
		self.updateSprite()

		if self.dead:
			if self.pos[1] - self.size[1] / 2 < self.level.size[0]:
				self.pos[1] += PYORO_DIE_SPEED * deltaTime

	def updateSprite(self):
		"""
		Define the sprite to use (normal, eating, jumping, catching, dying)
		"""

		if self.eatingCount:
			self.level.createActionDelay((self, "updateEatingCount"), \
				PYORO_EATING_DURATION, self.updateEatingCount)

		styleType = self.level.getStyleTypeWithScore()
		if self.dead:
			imageName = "pyoro_{}_die_{}.png"
		elif self.tongue:
			imageName = "pyoro_{}_eat_1_{}.png"
		elif self.notch:
			imageName = "pyoro_{}_jump_{}.png"
		elif self.eatingCount % 2:
			imageName = "pyoro_{}_eat_0_{}.png"
		else:
			imageName = "pyoro_{}_normal_{}.png"

		self.currentImageName = imageName.format(styleType, self.direction)

	def updateEatingCount(self):
		"""
		Update eating count value while in eating animation.
		"""

		self.eatingCount += 1
		if self.eatingCount < 8:
			self.level.setActionDelay((self, "updateEatingCount"), \
				PYORO_EATING_DURATION, self.updateEatingCount)
		else:
			self.eatingCount = 0
			self.level.removeActionDelay((self, "updateEatingCount"))

	def enableCapacity(self):
		"""
		Stop Pyoro and make him sticks out his tongue.
		"""

		if not(self.dead):
			self.sounds["pyoro_move"].pause()
			if self.tongue:
				self.tongue.remove()
			self.tongue = Tongue(self.level, self.direction)
			self.level.entities.append(self.tongue)

	def disableCapacity(self):
		"""
		Stop Pyoro from sticking out his tongue.
		"""

		if not(self.dead):
			if self.tongue:
				self.tongue.goBack = True

	def remove(self):
		"""
		Remove Pyoro's tongue and kill him starting its death animation.
		"""

		if not(self.dead):
			self.dead = True
			if self.tongue:
				self.tongue.remove()

			self.disableMove()
			
			self.level.removeActionDelay((self, "enableNotch"), \
				(self, "disableNotch"), (self, "updateEatingCount"))
			
			self.level.createActionDelay((self, "gameOver"), 1.28, \
				self.level.levelDrawer.activity.gameOver)
			self.level.createActionDelay((self, "removeGameOverActionDelay"), \
				1.29, self.level.removeActionDelay, (self, "gameOver"))
			
			self.level.getAudioPlayer().speed = 1
			self.sounds["pyoro_die"].play()
