# -*- coding: utf-8 -*-

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
Povides useful class for connecting, sending and receiving 
files on a FTPs server.

Created on 27/10/2018
"""

import os
import ftplib

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"


class FTP_manager:
	"""
	Simplify sending and downloading files on a FTPs server.
	"""

	def __init__(self, host, user = "", password = ""):
		"""
		Initialize a FTP_manager object. To connect it to the server,
		run FTP_manager.connect().

		:type host: str
		:param host: The host address (IP or DNS).

		:type user: str
		:param user: Optional. The username to use for login.

		:type password: str
		:param password: Optional. The password to use for login.
		"""

		self.stream = None
		self.connected = False
		self.host = host
		self.user = user
		self.password = password
		self.buffer = ""

	def __printError__(
				self, error, 
				methodName = "__printError__", 
				msg = "An error occured !"
			):
		"""
		Internal method used to display a specific message according to 
		a defined error.

		:type error: Exception
		:param error: The error to manage.

		:type methodName: str
		:param methodName: Optional. The FTP_manager method that had 
			an error.

		:type msg: str
		:param msg: Optional. A message to display.
		"""

		toDisplay = "%s%s"
		if isinstance(error, ftplib.error_temp):
			toDisplay = "[WARNING] [FTP_manager.%s] %s Temporary unvailable"
		elif isinstance(error, ftplib.error_perm):
			toDisplay = "[WARNING] [FTP_manager.%s]" \
				+ " %s Permanent error, check server file permission"
		elif isinstance(error, ftplib.error_proto):
			toDisplay = "[WARNING] [FTP_manager.%s]" \
				+ " %s The server reply does not fit the FTP specifications"
		elif isinstance(error, ftplib.error_reply):
			toDisplay = "[WARNING] [FTP_manager.%s]" \
				+ " %s Unexpected reply from the server"
		elif isinstance(error, IOError):
			toDisplay = "[WARNING] [FTP_manager.%s] %s " \
				+ "An error occured while writing in a local file"
		else:
			toDisplay = "[WARNING] [FTP_manager.%s] %s Unknown cause"
		print(toDisplay % (methodName, msg))

	def connect(self, user = None, password = None):
		"""
		Try to connect to the FTPs server.

		:type user: str
		:param user: Optional. If not defined, the default user is used.

		:type password: str
		:param password: Optional. If not defined, the default password
			is used.

		:rtype: bool
		:returns: True if it's a success, otherwise False.
		"""

		print("[INFO] [FTP_manager.connect] Connecting to the server")
		user = user if user else self.user
		password = password if password else self.password
		try:
			self.stream = ftplib.FTP_TLS(self.host, user, password)
			self.connected = True
			print("[INFO] [FTP_manager.connect] Connected successfuly !")
			return True
		except Exception as error:
			self.__printError__(error, "connect", 
				"Unable to connect or to login to the server !")
		self.connected = False
		return False

	def disconnect(self):
		"""
		Try to disconnect to the FTPs server.

		:rtype: bool
		:returns: True if it's a success, otherwise False.
		"""

		if self.connected:
			try:
				self.stream.quit()
				self.connected = False
				return True
			except Exception as error:
				self.__printError__(error, "disconnect", 
					"Unable to disconnect from the server !")
		else:
			print("[WARNING] [FTP_manager.disconnect]" \
				+ " Not connected to the server")
		return False

	def readServerFile(self, serverFilePath):
		"""
		Read a text file (utf-8 encoding) on the server.

		:type serverFilePath: str
		:param serverFilePath: The path to the file on the server.

		:rtype: str
		:returns: A string of the file content. 
			Empty string if something wrong happen.
		"""

		self.buffer = ""
		def write(binary):
			self.buffer += binary.decode()

		if self.connected:
			try:
				self.stream.retrbinary("RETR " + serverFilePath, write)
			except Exception as error:
				self.__printError__(error, "readServerFile", 
						"Unable to read \"%s\" from the server !" \
						% serverFilePath
					)
			return self.buffer
		print("[WARNING] [FTP_manager.readServerFile]" \
			+ " Not connected to the server")
		return ""

	def downloadFile(self, serverFilePath, localFilePath):
		"""
		Download a file from the server.

		:type serverFilePath: str
		:param serverFilePath: The path to the file on the server.

		:type localFilePath: str
		:param localFilePath: The path of the new local file.

		:rtype: bool
		:returns: True if it's a success, otherwise False.
		"""

		if self.connected:
			try:
				if not os.path.exists(os.path.dirname(localFilePath)):
					os.makedirs(os.path.dirname(localFilePath))

				with open(localFilePath, "wb") as file:
					self.stream.retrbinary(
							"RETR " + \
							serverFilePath, 
							file.write
						)
				
				return True
			except Exception as error:
				self.__printError__(error, "downloadFile", 
						"Unable to download \"%s\" from" % serverFilePath \
						+ " the server to \"%s\"!" % localFilePath
					)
		else:
			print("[WARNING] [FTP_manager.downloadFile]" \
				+ " Not connected to the server")
		return False

	def sendFile(self, localFilePath, serverFilePath):
		"""
		Send a file to the server.

		:type localFilePath: str
		:param localFilePath: The path of the local file to send.

		:type serverFilePath: str
		:param serverFilePath: The path to the new file on the server.

		:rtype: bool
		:returns: True if it's a success, otherwise False.
		"""

		if self.connected:
			try:

				with open(localFilePath, "rb") as file:
					self.stream.storbinary(
							"STOR " + \
							serverFilePath,
							file
						)
					
				return True
			except Exception as error:
				self.__printError__(error, "sendFile", 
						"Unable to send \"%s\"" % localFilePath \
						+ " to the server from \"%s\" !" % serverFilePath
					)
		else:
			print("[WARNING] [FTP_manager.sendFile]" \
				+ " Not connected to the server")
		return False

	def getServerFileNames(self, serverFolderPath = None):
		"""
		Get the names of all files and directories in a specific
		folder on the server.

		:type serverFolderPath: str
		:param serverFolderPath: Optional. The path to the folder
			on the server.

		:rtype: list<str>
		:returns: A list of file names.
		"""

		if self.connected:
			if not serverFolderPath:
				serverFolderPath = self.stream.pwd()
			try:
				return self.stream.nlst(serverFolderPath)
			except Exception as error:
				self.__printError__(error, "getServerFileNames", 
						"Unable to get file names in \"%s\" !" \
						% serverFolderPath
					)
		else:
			print("[WARNING] [FTP_manager.getServerFileNames]" \
				+ " Not connected to the server")
		return []

	def getCurrentDirectory(self):
		"""
		Get the current working directory path on the server.

		:rtype: str
		:returns: The path of the current working directory.
			Return an empty string if something wrong happen.
		"""

		if self.connected:
			return self.stream.pwd()
		print("[WARNING] FTP_manager.getCurrentDirectory]" \
			+ " Not connected to the server")
		return ""

	def setCurrentDirectory(self, serverPath):
		"""
		Set the working directory path.

		:type serverPath: str
		:param serverPath: The path to the new working directory.

		:rtype: bool
		:returns: True if it's a success, otherwise False.
		"""

		if self.connected:
			try:
				self.stream.cwd(serverPath)
				return True
			except Exception as error:
				self.__printError__(error, "setCurrentDirectory", 
						"Unable to define \"%s\" as the current directory !" \
						% serverPath
					)
		else:
			print("[WARNING] [FTP_manager.getCurrentDirectory]" \
				+ " Not connected to the server")
		return False

	def renameServerPath(self, fromName, toName):
		"""
		Rename a file or a folder on the server.

		:type fromName: str
		:param fromName: The path to the file or folder to rename.

		:type toName: str
		:param toName: The new path to give to the file 
			or folder to rename.

		:rtype: bool
		:returns: True if it's a success, otherwise False.
		"""

		if self.connected:
			try:
				self.stream.rename(fromName, toName)
				return True
			except Exception as error:
				self.__printError__(error, "renameServerPath", 
						"Unable to rename \"%s\" to \"%s\" !" \
						% (fromName, toName)
					)
		else:
			print("[WARNING] [FTP_manager.renameServerPath]" \
				+ " Not connected to the server")
		return False

	def removeServerFile(self, serverFilePath):
		"""
		Remove a file (doesn't work for folders) on the server.

		:type serverFilePath: str
		:param serverFilePath: The path to the file to remove.

		:rtype: bool
		:returns: True if it's a success, otherwise False.
		"""

		if self.connected:
			try:
				self.stream.delete(serverFilePath)
				return True
			except Exception as error:
				self.__printError__(error, "removeServerFile", 
						"Unable to remove \"%s\" from the server !" \
						% serverFilePath
					)
		else:
			print("[WARNING] [FTP_manager.removeServerFile] Not connected to the server")
		return False

	def removeServerDirectory(self, serverFolderPath):
		"""
		Remove a folder (doesn't work for a file) on the server.

		:type serverFolderPath: str
		:param serverFolderPath: The path to the folder to remove.

		:rtype: bool
		:returns: True if it's a success, otherwise False.
		"""

		if self.connected:
			try:
				self.stream.rmd(serverFolderPath)
				return True
			except Exception as error:
				self.__printError__(error, "removeServerDirectory", 
						"Unable to remove \"%s\" from the server !" \
						% serverFolderPath
					)
		else:
			print("[WARNING] [FTP_manager.removeServerDirectory]" \
				+ " Not connected to the server")
		return False

	def getFileSize(self, serverFilePath):
		"""
		Get the file of a file on the server.

		:type serverFilePath: str
		:param serverFilePath: The path to the file to get the size.

		:rtype: int
		:returns: The size of the file.
		"""

		if self.connected:
			try:
				return self.stream.size(serverFilePath)
			except Exception as error:
				self.__printError__(error, "getFileSize", 
						"Unable to get the size of \"%s\" !" \
						% serverFilePath
					)
		else:
			print("[WARNING] [FTP_manager.getFileSize]" \
				+ " Not connected to the server")
		return 0