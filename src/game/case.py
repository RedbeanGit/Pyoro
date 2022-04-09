# -*- coding:utf-8 -*-

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
Provide a simple class representing blocks on which Pyoro can walk.

Created on 17/03/2018
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"


class Case:
	"""
	A block on which Pyoro can walk. It can be destroyed and
	repaired by entities.angel.Angel.
	"""

	def __init__(self, pos):
		"""
		Initialize a Case object.

		:type pos: int
		:param pos: The horizontal position of the block.
		"""

		self.pos = pos
		self.exists = True
		self.isRepairing = False