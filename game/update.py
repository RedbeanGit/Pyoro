# -*- coding:utf-8 -*-

"""
Provide update functions

Created on 17/11/2018
"""

from game.config import VERSION, UPDATE_HOST, UPDATE_USER, UPDATE_PASSWORD
from game.ftp_manager import FTP_manager
from game.util import getExternalDataPath, copyDirectory

__author__ = "Julien Dubois"
__version__ = "1.1.1"

import os
import sys
import threading


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

	:rtype: list<str>
	:returns: A list of new versions. Return an empty list
		if something wrong happen.

	:Example: getUpdate(myftpMgr) -> ["1.2", "1.2.1", "1.3"]
	"""

	print("[INFO] [update.checkForUpdate] Checking for new updates")
	versions = ftpMgr.readServerFile("htdocs/game_update/versions.txt").split("\n")
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
	Download 
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


def getFilesToRemove(ftpMgr, version, folder = "htdocs/game_update/"):
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