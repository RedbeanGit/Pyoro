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
Provide update functions

Created on 17/11/2018
"""

import os
import sys
import threading

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import VERSION, UPDATE_HOST, UPDATE_USER, UPDATE_PASSWORD
from game.ftp_manager import FTP_manager
from game.util import getExternalDataPath, copyDirectory


def getConnectionStream():
	"""
	Create a new FTP_manager and try to connect it to the server.

	:rtype: game.ftp_manager.FTP_manager
	:returns: A new FTP_manager if successfully connected,
		otherwise None.
	"""

	ftp = FTP_manager(UPDATE_HOST, UPDATE_USER, UPDATE_PASSWORD)
	if ftp.connect():
		return ftp
	print("[WARNING] [update.getConnectionStream] Unable to" \
		+ " connect to the server")
	return None

def getUpdates(ftpMgr):
	"""
	Search new versions on a server.

	:type ftpMgr: game.ftp_manager.FTP_manager
	:param ftpMgr: The ftp manager used to download files.

	:rtype: list<str>
	:returns: A list of new versions. Return an empty list
		if something wrong happen.

	:Example: getUpdate(myftpMgr) -> ["1.2", "1.2.1", "1.3"]
	"""

	print("[INFO] [update.checkForUpdate] Checking for new updates")
	versions = ftpMgr.readServerFile("htdocs/game_update/versions.txt") \
		.split("\n")
	versionFound = False
	newVersions = []
	
	for version in versions:
		if versionFound:
			newVersions.append(version)
		if version == VERSION:
			versionFound = True
	return newVersions


def downloadUpdate(ftpMgr, version):
	"""
	Download files associated to a given version from the server.

	:type ftpMgr: game.ftp_manager.FTP_manager
	:param ftpMgr: The FTP_manager used to download files.

	:type version: str
	:param version: Version name (like "1.2.3")

	:rtype: bool
	:returns: False if an error occurs, True otherwise.
	"""

	print("[INFO] [update.downloadUpdate] Downloading update v" + version)
	downloadfp = getFilesToDownload(ftpMgr, version)
	removefp = getFilesToRemove(ftpMgr, version)
	serverFolder = "htdocs/game_update/" + version + "/"
	localFolder = os.path.join(getExternalDataPath(), "game_update")
	toReturn = True

	for filePath in downloadfp:
		serverFilePath = serverFolder + filePath
		localFilePath = os.path.join(localFolder, filePath.replace("/", "\\"))
		success = ftpMgr.downloadFile(serverFilePath, localFilePath)

		if not success:
			toReturn = False
	return toReturn


def getFilesToDownload(ftpMgr, version, folder = "htdocs/game_update/"):
	"""
	Get the name of the files to download for a defined version.

	:type ftpMgr: game.ftp_manager.FTP_manager
	:param ftpMgr: The FTP_manager to use.

	:type version: str
	:param version: The version to download.

	:type folder: str
	:param folder: Optional. The remote folder where to search the list 
		of files to download.

	:rtype: list<str>
	:returns: A list of file paths.
	"""

	toRemoveContent = ftpMgr.readServerFile(
		folder + version + "/toDownload.txt")
	if toRemoveContent:
		filePaths = toRemoveContent.split("\n")
		return filePaths
	return []


def getFilesToRemove(ftpMgr, version, folder="htdocs/game_update/"):
	"""
	Get the name of the files to remove for a defined version.

	:type ftpMgr: game.ftp_manager.FTP_manager
	:param ftpMgr: The FTP_manager to use.

	:type version: str
	:param version: In what version.

	:type folder: str
	:param folder: Optional. The remote folder where to search the list 
		of files to remove.

	:rtype: list<str>
	:returns: A list of file paths.
	"""

	toDownloadContent = ftpMgr.readServerFile(
		folder + version + "/toRemove.txt")
	if toDownloadContent:
		filePaths = toDownloadContent.split("\n")
		return filePaths
	return []


def getLibsDirectory():
	"""
	Get the lib folder path.

	:rtype: str
	:returns: The absolute path of the lib folder.
	"""

	if "lib" in os.listdir():
		return os.path.abspath("lib")
	return os.path.abspath("")


def installUpdate():
	"""
	Copy updated files to the installation directory.

	:rtype: bool
	:returns: True if installation is a success, otherwise False.
	"""

	print("[INFO] [update.installUpdate] Copying update files " \
		+ "into game installation folder")
	updateDirectory = os.path.join(getExternalDataPath(), "game_update")
	libDirectory = getLibsDirectory()
	toReturn = True

	if os.path.exists(updateDirectory):
		fileNames = os.listdir(updateDirectory)
		
		for fileName in fileNames:
			filePath = os.path.join(updateDirectory, fileName)
			
			if os.path.isdir(filePath) and fileName != "data":
				if not copyDirectory(filePath, 
						os.path.join(libDirectory, fileName)
					):
					print("[WARNING] [update.installUpdate] Something wrong" \
						+ "happened while copying files to install directory")
					toReturn = False
			else:
				if not copyDirectory(filePath, fileName):
					print("[WARNING] [update.installUpdate] Something wrong" \
						+ "happened while copying files to install directory")
					toReturn = False
	else:
		print("[WARNING] [update.installUpdate] No update found !")
		toReturn = False
	return toReturn