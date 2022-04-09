# -*- coding: utf-8 -*-

#   This file is part of Pyoro (A Python fan game).
#
#   Metawars is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Metawars is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
Provides a Pink_bean class.

Created on 21/03/2018
"""

import random

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.bean import Bean


class Pink_bean(Bean):
	"""
	Create pink beans. Pink beans have the hability to repair one case when
		cut or caught.
	"""

	def initImages(self):
		"""
		Load pink bean images.
		"""

		self.__initImages__("pink bean")
	
	def catch(self):
		"""
		Repair a case and the follow Pyoro tongue.
		"""

		self.level.repairCase()
		Bean.catch(self)
	
	def cut(self):
		"""
		Spawn pink leafs.
		"""

		self.sounds["bean_cut"].play()
		for i in range(2):
			randPos = [self.pos[0] + random.uniform(-0.5, 0.5), self.pos[1] + random.uniform(-0.5, 0.2)]
			self.level.spawnLeaf(randPos, "pink leaf")