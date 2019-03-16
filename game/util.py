# -*- coding:utf-8 -*-

"""
Provide useful functions

Created on 17/11/2018
"""

from game.config import DEFAULT_OPTIONS, NAME, VERSION

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import copy
import enum
import json
import os
import platform
import pygame
import sys

from gi.repository import Gdk
from lemapi.api import get_gui, restart_app, get_audio_player, get_save_path


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
	optionFolder = get_save_path()
	optionFilePath = os.path.join(optionFolder, "options.json")

	if not os.path.exists(optionFolder):
		os.makedirs(optionFolder)

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
	optionFilePath = os.path.join(get_save_path(), "options.json")
	if os.path.exists(optionFilePath):
		with open(optionFilePath, "r") as file:
			return json.load(file)
	return getDefaultOptions()


def getDefaultOptions():
	return copy.deepcopy(DEFAULT_OPTIONS)


def reset():
	"""
	Reset the game and restart.
	"""

	print("[INFO] [util.resetGame] Reseting game! Restarting...")
	optionFilePath = os.path.join(get_save_path(), "options.json")
	if os.path.exists(optionFilePath):
		os.remove(optionFilePath)
	Game.options = getDefaultOptions()
	restart_app()

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


def loadSounds():
	print("[INFO] [util.loadSounds] Loading sounds to RAM")
	soundPaths = getResourcePaths("sounds")
	ap = get_audio_player()
	for soundPath in soundPaths:
		sound = os.path.join("data", *soundPath)
		ap.load_sound(sound)
	musicPaths = getResourcePaths("musics")
	for musicPath in musicPaths:
		music = os.path.join("data", *musicPath)
		ap.load_music(music)


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

##############################################################################
### Enumerations #############################################################
##############################################################################


class Game:
	appId = 0
	options = None


class Errors(enum.Enum):
	MODULE_NOT_FOUND = 1
	DATA_NOT_FOUND = 2
	BOOT_ERROR = 3
	LOOP_ERROR = 4
	UPDATE_ERROR = 5
	BAD_RESOURCE = 6
	CODE_ERROR = 7
