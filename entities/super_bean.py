# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 17/03/2018
	@version: 1
=========================
"""

import random

from entities.bean import Bean
from game.config import BEAN_SPRITE_DURATION

class Super_bean(Bean):
	def __init__(self, level, pos, speed):
		self.spriteIndex = 0
		self.colorIndex = 0
		Bean.__init__(self, level, pos, speed)

	def initImages(self):
		self.__initImages__("super bean")

	def initSounds(self):
		Bean.initSounds(self)
		self.__initSounds__(("bean_implode",))
	
	def updateSprite(self):
		if not self.colorIndex % 2:
			self.spriteIndex = self.spriteIndex + 1 if self.spriteIndex < 2 else 0
		self.colorIndex = self.colorIndex + 1 if self.colorIndex < 5 else 0
		self.currentImageName = "bean_{}_{}.png".format(self.spriteIndex, self.colorIndex)
		self.level.setActionDelay((self, "updateSprite"), BEAN_SPRITE_DURATION / 6, self.updateSprite)
	
	def catch(self):
		i = 0
		for entity in self.level.entities:
			if isinstance(entity, Bean) and entity != self:
				self.level.createActionDelay((self, "destroyBean", i), i * 0.1, self.destroyBean, entity, i)
				i += 1
		i = 0
		emptyCases = list(self.level.getVoidCases())
		for i in range(min(10, len(emptyCases))):
			self.level.createActionDelay((self, "repairCase", emptyCases[i].pos), i * 0.5, self.repairCase, emptyCases[i])
		Bean.catch(self)

	def destroyBean(self, bean, beanId):
		self.sounds["bean_implode"].play()
		bean.cut()
		bean.remove()
		self.level.spawnScore(50, bean.pos)
		self.level.removeActionDelay((self, "destroyBean", beanId))

	def cut(self):
		self.sounds["bean_cut"].play()
		for i in range(2):
			randPos = [self.pos[0] + random.uniform(-0.5, 0.5), self.pos[1] + random.uniform(-0.5, 0.2)]
			self.level.spawnLeaf(randPos, "super leaf")

	def repairCase(self, case):
		self.level.repairCase(case)
		self.level.removeActionDelay((self, "repairCase", case.pos))

	def remove(self):
		self.level.removeActionDelay(("override", self, "updateSprite"))
		Bean.remove(self)