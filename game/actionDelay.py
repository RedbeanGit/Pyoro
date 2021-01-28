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
Provide a class to delay the call of a
function of method.

Created on 14/08/2018
"""

import time

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"


class ActionDelay:
	"""
	Delay the call of a function or method of a defined time.
	"""

	def __init__(self, waitTime, fct, *fctArgs, **fctKwargs):
		"""
		Initialize an ActionDelay object.

		:type waitTime: float
		:param waitTime: Delay (in second).

		:type fct: function, method
		:param fct: The function or method to call.

		:type *fctArgs: objects
		:param *fctArgs: The arguments to pass to the function
			or method to run.

		:type **fctKwargs: objects
		:param **fctKwargs: The optional arguments to pass to
			the function or method to run.
		"""

		self.waitTime = waitTime
		self.passedTime = 0
		self.fct = fct
		self.fctArgs = fctArgs
		self.fctKwargs = fctKwargs
		self.lastTime = time.time()

	def update(self, deltaTime):
		"""
		Update the timer.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last update.
		"""

		self.passedTime += deltaTime
		if self.passedTime >= self.waitTime:
			self.fct(*self.fctArgs, **self.fctKwargs)