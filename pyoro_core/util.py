# -*- coding:utf-8 -*-

"""
Provide useful functions

Created on 17/11/2018
"""

from pyoro_core.constants import DEFAULT_OPTIONS, NAME, VERSION, Game, Errors

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import copy
import json
import os

from lemapi.api import get_gui, restart_app, get_audio_player, get_save_path


##############################################################################
### Options ##################################################################
##############################################################################


def saveOptions():
	print("[Pyoro] [INFO] [saveOptions] Saving game options")
	optionFolder = get_save_path()
	optionFilePath = os.path.join(optionFolder, "options.json")

	if not os.path.exists(optionFolder):
		os.makedirs(optionFolder)

	with open(optionFilePath, "w") as file:
		json.dump(Game.OPTIONS, file, indent="\t")


def loadOptions():
	print("[Pyoro] [INFO] [loadOptions] Loading game options")
	optionFilePath = os.path.join(get_save_path(), "options.json")

	if os.path.exists(optionFilePath):
		with open(optionFilePath, "r") as file:
			Game.OPTIONS = json.load(file)
	else:
		print("[Pyoro] [WARNING] [loadOptions] Unable to find 'options.json'! Using default options")
		Game.OPTIONS = getDefaultOptions()


def getDefaultOptions():
	return copy.deepcopy(DEFAULT_OPTIONS)


def reset():
	print("[Pyoro] [INFO] [resetGame] Reseting game and restarting...")
	optionFilePath = os.path.join(get_save_path(), "options.json")

	if os.path.exists(optionFilePath):
		os.remove(optionFilePath)
	
	Game.OPTIONS = getDefaultOptions()
	restart_app()

##############################################################################
### Data and modules managment ###############################################
##############################################################################


def loadImages():
	print("[Pyoro] [INFO] [loadImages] Loading images to RAM")
	imagePaths = getResourcePaths("images")
	gui = get_gui()

	for imagePath in imagePaths:
		image = os.path.join("data", *imagePath)
		gui.load_image(image)


def loadSounds():
	print("[Pyoro] [INFO] [loadSounds] Loading sounds to RAM")
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
	print("[Pyoro] [INFO] [getResourcePaths] Detecting '%s' resources" % resourceType)
	resFilePath = os.path.join("data", "resources.json")

	if os.path.exists(resFilePath):
		with open(resFilePath, "r") as file:
			resources = json.load(file)

			if resourceType in resources:
				return resources[resourceType]
			print("[Pyoro] [WARNING] [getResourcePaths] '%s'" % resourceType \
				+ " is not a valid resource type")
	else:
		print("[Pyoro] [WARNING] [getResourcePaths] Unable to find '%s'" % resFilePath)
	
	leaveGame(Errors.BAD_RESOURCE)