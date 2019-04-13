# -*- coding: utf-8 -*-

"""
Provides a class to create a red bird managed by the computer

Created on 11/04/2018
"""

from pyoro_entities.bean import Bean
from pyoro_entities.pyoro import Pyoro

__author__ = "Julien Dubois"
__version__ = "2.0.0"


class Pyobot(Pyoro):
	def __init__(self, level):
		Pyoro.__init__(self, level)

	def update(self, deltaTime):
		if not self.tong:
			pos = self.getNearestPos(*self.getPosToEat())
			if pos > 0 and pos < self.level.size[0]:
				if self.pos[0] > pos:
					self.enableMoveLeft()
				elif self.pos[0] < pos:
					self.enableMoveRight()
			else:
				self.disableMove()

			if int(pos) == int(self.pos[0]):
				self.lookBean()
				self.enableCapacity()
		Pyoro.update(self, deltaTime)

	def getPosToEat(self):
		lowestBean = self.getLowestBean()
		if lowestBean:
			return [lowestBean.pos[0] - (self.level.size[1] - lowestBean.pos[1]), \
				lowestBean.pos[0] + (self.level.size[1] - lowestBean.pos[1])]
		else:
			return [-1, self.level.size[0]]

	def lookBean(self):
		lowestBean = self.getLowestBean()
		if lowestBean:
			if self.pos[0] > lowestBean.pos[0]:
				self.enableMoveLeft()
			else:
				self.enableMoveRight()
		self.disableMove()

	def getNearestPos(self, pos1, pos2):
		pos = sorted([pos1, pos2], key = lambda x: abs(self.pos[0] - x))
		if pos[0] <= 0 or pos[0] >= self.level.size[0]:
			return pos[1]
		return pos[0]

	def remove(self):
		self.level.reset()

	def getLowestBean(self):
		bestEntity = None
		for entity in self.level.entities:
			if isinstance(entity, Bean):
				if bestEntity == None:
					bestEntity = entity
				elif entity.pos[1] > bestEntity.pos[1]:
					bestEntity = entity
		return bestEntity
