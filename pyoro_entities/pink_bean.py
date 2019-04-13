# -*- coding: utf-8 -*-

"""
Provides a class to create pink beans.

Created on 21/03/2018
"""

from pyoro_entities.bean import Bean

__author__ = "Julien Dubois"
__version__ = "2.0.0"

import random


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
