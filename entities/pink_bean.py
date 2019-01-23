# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 21/03/2018
	@version: 1
=========================
"""

import random

from entities.bean import Bean

class Pink_bean(Bean):
	def initImages(self):
		imageNames = []
		for i in range(3):
			for j in range(3):
				imageNames.append("bean_%s_%s.png" % (i, j))
		self.__initImages__("pink bean", imageNames)

	def catch(self):
		self.level.repairCase()
		Bean.catch(self)

	def cut(self):
		self.sounds["bean_cut"].play()
		for i in range(2):
			randPos = [self.pos[0] + random.uniform(-0.5, 0.5), self.pos[1] + random.uniform(-0.5, 0.2)]
			self.level.spawnLeaf(randPos, "pink leaf")
