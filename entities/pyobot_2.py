# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 01/09/2018
	@version: 1.1
=========================
"""

from entities.bean import Bean
from entities.pyoro_2 import Pyoro_2

class Pyobot_2(Pyoro_2):
	def __init__(self, level):
		Pyoro_2.__init__(self, level)

	def update(self, deltaTime):
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
		Pyoro_2.update(self, deltaTime)

	def getPosToEat(self):
		lowestBean = self.getLowestBean()
		if lowestBean:
			return [lowestBean.pos[0] - (self.level.size[0] - lowestBean.pos[1]), \
				lowestBean.pos[0] + (self.level.size[0] - lowestBean.pos[1])]
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
		for entity in self.level.entities:
			if isinstance(entity, Bean):
				return entity
		return None
