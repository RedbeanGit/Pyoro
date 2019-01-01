# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 18/03/2018
	@version: 1
=========================
"""

from entities.entity import Entity
from entities.tong import Tong
from game.config import PYORO_SPEED, PYORO_NOTCH_DURATION, PYORO_EATING_DURATION, \
	PYORO_DIE_SPEED

class Pyoro(Entity):
	def __init__(self, level):
		self.moving = False
		self.notch = False
		self.dead = False
		self.tong = None
		self.eatingCount = 0
		self.direction = 1
		w, h = level.size
		Entity.__init__(self, level, (2, h - 2), (2, 2))

	def initImages(self):
		self.__initImages__("pyoro 1")

	def initSounds(self):
		self.__initSounds__(("pyoro_move", "pyoro_die"))

	# directions
	def enableMoveRight(self):
		if not(self.dead) and not(self.tong):
			self.direction = 1
			self.moving = True
			self.sounds["pyoro_move"].play(-1)

	def enableMoveLeft(self):
		if not(self.dead) and not(self.tong):
			self.direction = -1
			self.moving = True
			self.sounds["pyoro_move"].play(-1)

	def disableMove(self):
		if self.sounds["pyoro_move"].isPlaying:
			self.sounds["pyoro_move"].pause()
		self.moving = False
		self.notch = False

	def move(self, deltaTime):
		if not(self.dead) and not(self.tong):
			if not self.notch:
				if self.direction == 1:
					newPos = self.pos[0] + self.size[0] / 2 + PYORO_SPEED * deltaTime
					voidPos = self.getVoidCasePosOnPath(newPos)

					if newPos >= self.level.size[0]:
						self.pos[0] = self.level.size[0] - self.size[0] / 2
					elif voidPos != None:
						self.pos[0] = voidPos - self.size[0] / 2
					else:
						self.pos[0] += PYORO_SPEED * deltaTime

				else:
					newPos = self.pos[0] - self.size[0] / 2 - PYORO_SPEED * deltaTime
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
		self.notch = True
		self.level.removeActionDelay((self, "enableNotch"))
		self.level.createActionDelay((self, "disableNotch"), \
			PYORO_NOTCH_DURATION, self.disableNotch)

	def disableNotch(self):
		self.notch = False
		self.level.removeActionDelay((self, "disableNotch"))

	# update method
	def update(self, deltaTime):
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
		if self.eatingCount:
			self.level.createActionDelay((self, "updateEatingCount"), \
				PYORO_EATING_DURATION, self.updateEatingCount)
		styleType = self.level.getStyleTypeWithScore()
		if self.dead:
			self.currentImageName = "pyoro_{}_die_{}.png".format(styleType, self.direction)
		elif self.tong:
			self.currentImageName = "pyoro_{}_eat_1_{}.png".format(styleType, self.direction)
		elif self.notch:
			self.currentImageName = "pyoro_{}_jump_{}.png".format(styleType, self.direction)
		elif self.eatingCount % 2:
			self.currentImageName = "pyoro_{}_eat_0_{}.png".format(styleType, self.direction)
		else:
			self.currentImageName = "pyoro_{}_normal_{}.png".format(styleType, self.direction)

	def updateEatingCount(self):
		self.eatingCount += 1
		if self.eatingCount < 8:
			self.level.setActionDelay((self, "updateEatingCount"), \
				PYORO_EATING_DURATION, self.updateEatingCount)
		else:
			self.eatingCount = 0
			self.level.removeActionDelay((self, "updateEatingCount"))

	def enableCapacity(self):
		if not(self.dead):
			self.sounds["pyoro_move"].pause()
			if self.tong:
				self.tong.remove()
			self.tong = Tong(self.level, self.direction)
			self.level.entities.append(self.tong)

	def disableCapacity(self):
		if not(self.dead):
			if self.tong:
				self.tong.goBack = True

	def remove(self):
		if not(self.dead):
			self.dead = True
			if self.tong:
				self.tong.remove()
			self.disableMove()
			self.level.removeActionDelay((self, "enableNotch"), \
				(self, "disableNotch"), (self, "updateEatingCount"))
			self.level.getAudioPlayer().speed = 1
			self.sounds["pyoro_die"].play()
			self.level.createActionDelay((self, "gameOver"), 1.28, \
				self.level.levelDrawer.activity.gameOver)
			self.level.createActionDelay((self, "removeGameOverActionDelay"), \
				1.29, self.level.removeActionDelay, (self, "gameOver"))
