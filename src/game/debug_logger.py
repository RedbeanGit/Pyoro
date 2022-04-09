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
Provide a Debug_logger class to manage outputs debug logs.

Created on 15/08/2018
"""

import sys
import time
import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import DEBUG
from game.util import getExternalDataPath


class Debug_logger:
	"""
	Replace the default output (sys.stdout). Write debug log files and
	display output messages.
	"""

	def __init__(self):
		"""
		Initialize a Debug_logger object.
		"""

		self.message = []
		self.logFolder = getExternalDataPath()
		self.logFile = self.getLogFile()
		sys.stdout = self
		print("[INFO] [Debug_logger.__init__] Starting Debug_logger")

	def getLogFile(self):
		"""
		Get the relative path of a new debug log.

		:rtype: _io.TextIOWrapper
		:returns: A new file opened in text write mode.
		"""

		if not os.path.exists(os.path.join(self.logFolder, "logs")):
			os.makedirs(os.path.join(self.logFolder, "logs"))
		logId = 1
		date = time.localtime()
		filePath = os.path.join(self.logFolder, "logs", "{}-{}-{}-{}.txt".format(date.tm_year, date.tm_mon, date.tm_mday, logId))
		while os.path.exists(filePath):
			logId += 1
			filePath = os.path.join(self.logFolder, "logs", "{}-{}-{}-{}.txt".format(date.tm_year, date.tm_mon, date.tm_mday, logId))
		return open(filePath, "w")

	def write(self, message):
		"""
		Write something to the debug log and default output.

		:type message: str
		:param message: A string to write.
		"""

		self.message.append(message)
		if DEBUG and sys.__stdout__:
			sys.__stdout__.write(message)
		if message == "\n":
			self.logFile.write("\n")
		else:
			date = time.localtime()
			self.logFile.write("[{}:{}:{}] {}".format(date.tm_hour, date.tm_min, date.tm_sec, message))

	def flush(self):
		"""
		Flush the default output (sys.stdout).
		"""

		if sys.__stdout__:
			sys.__stdout__.flush()

	def close(self):
		"""
		Close the default output (sys.stdout).
		"""

		sys.stdout = sys.__stdout__
		self.logFile.close()