# -*- coding:utf-8 -*-

"""
Provide useful functions

Created on 17/11/2018
"""

from game.config import DEFAULT_OPTIONS, NAME, VERSION

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import ctypes
import enum
import json
import os
import platform
import pygame
import shutil
import subprocess
import sys
import threading

from gi.repository import Gdk
from pygame.locals import K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, \
	K_q, K_w, K_z, K_m, K_a, K_MINUS, K_LEFTBRACKET, K_RIGHTBRACKET, \
	K_SEMICOLON, K_QUOTE, K_COMMA, K_PERIOD, K_SLASH, JOYBUTTONDOWN, \
	JOYHATMOTION, JOYAXISMOTION

##############################################################################
### Input representation #####################################################
##############################################################################

def getKeyName(keyCode):
	"""
	Get azerty equivalent of a key from a qwerty keyboard

	:type keyCode: int
	:param keyCode: The pygame code of a key.

	:rtype: str
	:returns: A key representation.
	"""

	newKeys = {
		K_1: "&", K_2: "é", K_3: "\"", K_4: "'",
		K_5: "(", K_6: "-", K_7: "è", K_8: "_",
		K_9: "ç", K_0: "à", K_MINUS: ")", K_q: "a",
		K_w: "z", K_LEFTBRACKET: "^", K_RIGHTBRACKET: "$", K_a: "q",
		K_SEMICOLON: "m", K_QUOTE: "ù", K_z: "w", K_m: ",",
		K_COMMA: ";", K_PERIOD: ":", K_SLASH: "!"
	}

	if keyCode in newKeys:
		return newKeys[keyCode]
	return pygame.key.name(keyCode)


def getJoyKeyName(inputType, **inputKwargs):
	"""
	Get a representation of a joystick input.

	:type inputType: int
	:param inputType: The pygame code of a joystick input type.
		It can be JOYBUTTONDOWN, JOYHATMOTION or JOYAXISMOTION.

	:type **inputKwargs: object
	:param **inputKwargs: Some data about the input.

	:rtype: str
	:returns: A representation of the joystick input.
	"""

	if inputType == JOYBUTTONDOWN:
		if "buttonId" not in inputKwargs:
			inputKwargs["buttonId"] = "inconnu"
		return "Bouton {}".format(inputKwargs["buttonId"])
	elif inputType == JOYHATMOTION:
		if "value" not in inputKwargs:
			inputKwargs["value"] = (0, 0)
		inputKwargs["value"] = tuple(inputKwargs["value"])
		if inputKwargs["value"] == (-1, 0):
			return "gauche"
		elif inputKwargs["value"] == (1, 0):
			return "droite"
		elif inputKwargs["value"] == (0, -1):
			return "bas"
		elif inputKwargs["value"] == (0, 1):
			return "haut"
		else:
			return "direction ?"
	elif inputType == JOYAXISMOTION:
		if "axisId" not in inputKwargs:
			inputKwargs["axisId"] = 0
		if "value" not in inputKwargs:
			inputKwargs["value"] = 0
		if inputKwargs["axisId"] == 0:
			if inputKwargs["value"] < 0:
				return "gauche"
			elif inputKwargs["value"] > 0:
				return "droite"
			else:
				return "direction ?"
		elif inputKwargs["axisId"] == 1:
			if inputKwargs["value"] < 0:
				return "haut"
			elif inputKwargs["value"] > 0:
				return "bas"
			else:
				return "direction ?"

##############################################################################
### Options ##################################################################
##############################################################################


def saveOptions(options):
	"""
	Save options in a json file.

	:type options: dict
	:param options: A dictionary with data to save.
	"""

	print("[INFO] [util.saveOptions] Saving game options")
	optionFilePath = os.path.join(getExternalDataPath(), "options.json")
	with open(optionFilePath, "w") as file:
		json.dump(options, file, indent = "\t")


def loadOptions():
	"""
	Load options from a json file. If no option found, return
	game.config.DEFAULT_OPTIONS.

	:rtype: dict
	:returns: A dictionary of saved data.
	"""

	print("[INFO] [util.loadOptions] Loading game options")
	optionFilePath = os.path.join(getExternalDataPath(), "options.json")
	if os.path.exists(optionFilePath):
		with open(optionFilePath, "r") as file:
			return json.load(file)
	return DEFAULT_OPTIONS

##############################################################################
### Leave, reset and restart #################################################
##############################################################################


def stopGame():
	"""
	Stop the audio player, the debug logger and close the current window.
	"""

	print("[INFO] [util.stopGame] Stopping %s" % NAME.capitalize())
	pygame.quit()
	if Game.audioPlayer:
		Game.audioPlayer.stop()
	if Game.debugLogger:
		Game.debugLogger.close()


def leaveGame(errorId = 0):
	"""
	Stop the game and send an error message if something
	wrong happened.

	:type errorId: int
	:param errorId: Optional. An error id. 0 is used if
		not defined.
	"""

	print("[INFO] [util.leaveGame] Leaving %s v%s" % (NAME.capitalize(), VERSION))
	stopGame()

	if errorId == 0:
		sys.exit()
	if errorId == Errors.MODULE_NOT_FOUND:
		raise ImportError("Une erreur est survenue ! " \
			+ "Il semblerait qu'un module Python essentiel" \
			+ " au fonctionnement du jeu soit absent")
	elif errorId == Errors.DATA_NOT_FOUND:
		raise RuntimeError("Une erreur est survenue ! " \
			+ "Il manque les données du jeu " \
			+ "(images, sons, polices d'écriture, ...) !")
	elif errorId == Errors.BOOT_ERROR:
		raise RuntimeError("Une erreur est survenue pendant" \
			+ " le démarrage du jeu ! Consultez " \
			+ "les logs pour plus de détails")
	elif errorId == Errors.LOOP_ERROR:
		raise RuntimeError("Une erreur est survenue pendant la" \
			+ " boucle de jeu ! Consultez les " \
			+ "logs pour plus de détails")
	elif errorId == Errors.UPDATE_ERROR:
		raise RuntimeError("Une erreur est survenue pendant l'installation" \
			+ " des mises à jours ! Consultez les " \
			+ "logs pour plus de détails")
	raise RuntimeError("Une erreur inconnue est survenue " \
		+ "(errorId=%s) ! Consultez les logs pour plus de détails" % errorId)


def restart(*args):
	"""
	Restart the game with defined arguments.

	:type *args: str
	:param *args: The arguments to pass on reboot.
	"""

	print("[INFO] [util.restart] Restarting game")
	if sys.executable == sys.argv[0]:
		subprocess.Popen([sys.executable] + list(args))
	else:
		subprocess.Popen([sys.executable, sys.argv[0]] + list(args))
	leaveGame()


def adminRestart(*args):
	"""
	Restart by requesting administrator or root privileges.

	:type *args: str
	:param *args: The arguments to pass on reboot.
	"""

	print("[INFO] [util.adminRestart] Restarting game with admin elevation")
	systemName = platform.system()
	args = list(args)

	if sys.executable != sys.argv[0]:
		args.insert(0, sys.argv[0])

	def uacPrompt():
		ctypes.windll.shell32.ShellExecuteW(
				None,
				"runas",
				sys.executable,
				" ".join(args),
				None,
				1
			)

	def rootPrompt():
		toReturn = 0
		# If the user isn't a super user
		if os.geteuid() != 0:
			msg = "[sudo] password for %u:"
			toReturn = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)
		return toReturn

	if systemName == "Windows":
		threading.Thread(target = uacPrompt).start()
		leaveGame()
	else:
		if rootPrompt() == 0:
			restart()
		else:
			print("[WARNING] [util.adminRestart] Unable to get root privileges")
			leaveGame()


def resetGame():
	"""
	Reset the game and restart.
	"""

	print("[INFO] [util.resetGame] Reseting game! Restarting...")
	optionFilePath = os.path.join(getExternalDataPath(), "options.json")
	if os.path.exists(optionFilePath):
		os.remove(optionFilePath)
	restart()

##############################################################################
### Data and modules managment ###############################################
##############################################################################


def checkData():
	"""
	Check if there is resources.json file.

	:rtype: bool
	:returns: True if found, otherwise False.
	"""

	print("[INFO] [util.checkData] Checking data")
	return os.path.exists(os.path.join("data", "resources.json"))


def checkModules():
	"""
	Check needed python modules.

	:rtype: bool
	:returns: True if all needed modules are installed, otherwise False.
	"""

	print("[INFO] [util.chechModules] Checking required modules")
	required = ("os", "sys", "pygame", "json", "wave", "audioop", "pyaudio",
		"threading", "traceback", "time", "platform", "shutil", "ftplib",
		"enum", "gi")

	for moduleName in required:
		try:
			print("[INFO] [util.chechModules] Checking \"%s\"" % moduleName)
			exec("import " + moduleName)
		except ImportError:
			print("[WARNING] [util.chechModules] No module " \
				+ '"%s" detected !' % moduleName)
			return False
	return True


def getResourcePaths(resourceType):
	"""
	Get the path of all resources in a defined category.

	:type resourceType: str
	:param resourceType: The category of resource. It can be
		"musics", "sounds" and "images"

	:rtype: list<str>
	:returns: A list of paths to files of the specified category.
		If somethinf wrong happen, return an empty list.
	"""

	print("[INFO] [util.getResourcePaths] " \
		+ "Detecting \"%s\" resources" % resourceType)
	resFilePath = os.path.join("data", "resources.json")
	if os.path.exists(resFilePath):
		with open(resFilePath, "r") as file:
			resources = json.load(file)
			if resourceType in resources:
				return resources[resourceType]
			print("[WARNING] [util.getResourcePaths] \"%s\"" % resourceType \
				+ " is not a valid resource type")
	else:
		print("[WARNING] [util.getResourcePaths] " \
			+ "Unable to find \"%s\"" % resFilePath)
	return []


def getExternalDataPath():
	r"""
	Get the path to the game data folder according to the host
	operating system.
		- %AppData%\Pyoro on Window
		- /home/<user>/share/Pyoro on Linux distributions
		- /home/<user>/Library/Pyoro on MacOS.
	"""

	systemName = platform.system()
	if systemName == "Windows":
		return os.path.join(
				os.environ["APPDATA"],
				NAME.capitalize()
			)
	elif systemName == "Linux":
		return os.path.join(
				os.path.expanduser("~"),
				"share",
				NAME.capitalize()
			)
	elif systemName == "Darwin":
		return os.path.join(
				os.path.expanduser("~"),
				"Library",
				NAME.capitalize()
			)
	print("[WARNING] [util.getExternalDataPath] Unknown operating system")
	return "saves"


def copyDirectory(fromPath, toPath):
	"""
	Recursion copy file or folder.

	:type fromPath: str
	:param fromPath: The folder path to copy from.

	:type toPath: str
	:param toPath: The destination file or folder.

	:rtype: bool
	:returns: True if files and folders has been copied successfuly,
		otherwise False.
	"""

	print("[INFO] [util.copyDirectory] Copying folder " \
		+ "%s to %s" % (fromPath, toPath))
	toReturn = True

	if os.path.isdir(fromPath):
		fileNames = os.listdir(fromPath)
		for fileName in fileNames:
			sourceFilePath = os.path.join(fromPath, fileName)
			newFilePath = os.path.join(toPath, fileName)
			if not copyDirectory(sourceFilePath, newFilePath):
				toReturn = False
	else:
		if os.path.exists(fromPath):
			if not os.path.exists(os.path.dirname(toPath)):
				os.makedirs(os.path.dirname(toPath))

			try:
				shutil.copyfile(fromPath, toPath)
			except Exception:
				print("[WARNING] [util.copyDirectory] Error while copying" \
					" %s to %s ! Ignoring it" % (fromPath, toPath))
				toReturn = False
		else:
			print("[WARNING] [util.copyDirectory] File " \
				"\"%s\" doesn't exist" % fromPath)
			toReturn = False

	return toReturn

##############################################################################
### Screen Infos #############################################################
##############################################################################


def getLayoutTemplate(ratio):
	"""
	Get the best layout for a given ratio.

	:type ratio: float
	:param ratio: The ratio of the game window.

	:rtype: dict
	:returns: A dictionary representing placement informations about
		the graphical components of the game menu.
	"""

	# Detecting best layout name accourding to the resolution
	if ratio > 1:
		bestLayoutName = "Wide"
	elif ratio < 1:
		bestLayoutName = "Narrow"
	else:
		bestLayoutName = "Square"

	layoutFilePath = os.path.join("data", "layouts.json")
	if os.path.exists(layoutFilePath):
		with open(layoutFilePath, "r") as file:
			layouts = json.load(file)

			# Searching the best layout
			for layout in layouts:
				if "name" in layout:
					if layout["name"] == bestLayoutName:
						print("[INFO] [util.getLayoutTemplate] Layout" \
							+ ' "%s" choosen' % bestLayoutName)
						return layout
				else:
					print("[WARNING] [util.getLayoutTemplate] Some layouts" \
						+ " aren't named")

		print("[WARNING] [util.getLayoutTemplate] Unable to find a layout" \
			+ " which fit the given ratio")
	else:
		print("[WARNING] [util.getLayoutTemplate] Unable" \
			+ ' to find "%s"' % layoutFilePath)
	return {}


def getMonitorSize():
	"""
	Return the screen size in mm.

	:rtype: tuple
	:returns: (width, height) tuple where width and height are ints which
		represent the default screen size in millimeters.
	"""

	display = Gdk.Display.get_default()
	monitor = display.get_monitor(0)
	return monitor.get_width_mm(), monitor.get_height_mm()

def getScreenSize():
	"""
	Return the screen size in pixels.

	:rtype: tuple
	:returns: (width, height) tuple where width and height are ints which
		represent the default screen size in pixels.
	"""

	screen = Gdk.Screen.get_default()
	return screen.get_width(), screen.get_height()

def getScreenRatio():
	"""
	Return the screen resolution (width / height).

	:rtype: float
	:returns: A floating point value representing the ratio width / height.
	"""

	w, h = getScreenSize()
	if h:
		return w / h
	print("[WARNING] [util.getScreenRatio] Height can't be null")
	return 1


##############################################################################
### Enumerations #############################################################
##############################################################################

class Game:
	window = None
	debugLogger = None
	audioPlayer = None

class Errors(enum.Enum):
	MODULE_NOT_FOUND = 1
	DATA_NOT_FOUND = 2
	BOOT_ERROR = 3
	LOOP_ERROR = 4
	UPDATE_ERROR = 5
