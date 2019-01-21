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
from lemapi.api import get_gui, restart_app
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


def reset():
	"""
	Reset the game and restart.
	"""

	print("[INFO] [util.resetGame] Reseting game! Restarting...")
	optionFilePath = os.path.join(getExternalDataPath(), "options.json")
	if os.path.exists(optionFilePath):
		os.remove(optionFilePath)
	restart_app(Game.appId)

##############################################################################
### Data and modules managment ###############################################
##############################################################################


def loadImages():
	print("[INFO] [util.loadImages] Loading images to RAM")
	imagePaths = getResourcePaths("images")
	gui = get_gui()
	for imagePath in imagePaths:
		image = os.path.join("data", *imagePath)
		gui.load_image(image)


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
	leaveGame(Errors.BAD_RESOURCE)


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

##############################################################################
### Screen Infos #############################################################
##############################################################################


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


def getMonitorDensity():
	wm, hm = getMonitorSize()
	wp, hp = getScreenSize()
	return wp / wm, hp / hm


##############################################################################
### Enumerations #############################################################
##############################################################################


class Game:
	appId = 0
	audioPlayer = None
	options = None


class Errors(enum.Enum):
	MODULE_NOT_FOUND = 1
	DATA_NOT_FOUND = 2
	BOOT_ERROR = 3
	LOOP_ERROR = 4
	UPDATE_ERROR = 5
	BAD_RESOURCE = 6
	CODE_ERROR = 7
