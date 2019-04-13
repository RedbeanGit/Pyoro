# -*- coding:utf-8 -*-

"""
Provide a class to delay the call of a
function of method.

Created on 14/08/2018
"""

__author__ = "Julien Dubois"
__version__ = "1.1"

import time


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