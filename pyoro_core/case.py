# -*- coding:utf-8 -*-

"""
Provide a simple class representing blocks on which Pyoro can walk.

Created on 17/03/2018
"""

__author__ = "Julien Dubois"
__version__ = "1.1"


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