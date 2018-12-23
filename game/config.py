# -*- coding: utf-8 -*-

"""
Provide useful constants used in the game.

Created on 17/03/2018
"""

__author__ = "Julien Dubois"
__version__ = "1.1"

import os


# General information about the game
DEBUG = True														# Debugging mode (if you want to see logs in a console)
FPS = 60															# frame per seconds
HEIGHT = 640														# window height in pixels
NAME = "PYORO"														# game name
VERSION = "1.1.1"													# game version
WIDTH = 640															# window width in pixels

# Update server address and login
UPDATE_HOST = "ftpupload.net"										# FTP host
UPDATE_USER = "epiz_22757918"										# FTP username
UPDATE_PASSWORD = "6UJDteWTmclaL"									# FTP password

# Some level constants
AIR_RESISTANCE = 25													# Air resistance value for leaf and seeds wind effect
BACKGROUND_TRANSITION_DURATION = 3									# Speed of transition between to backgrounds
CASE_SIZE = 32														# Size of a block (in pixels)
GRAVITY_FORCE = 9.81												# Gravity force for seeds falling effect
SPEED_ACCELERATION = 0.01											# Acceleration of the level speed each second
BACKGROUND_ANIMATED_DURATION = 1									# Duration of each animated background (for last backgrounds)
SPLASH_ANIMATION_DURATION = 0.125									# Duration of each animation during splash screen (currently useless)

# Main file paths
GUI_IMAGE_PATH = os.path.join("data", "images", "gui")				# File path to Graphical User Interface images
ENTITIES_IMAGE_PATH = os.path.join("data", "images", "entities")	# File path to entities images
LEVEL_IMAGE_PATH = os.path.join("data", "images", "level")			# File path to level images (backgrounds, blocks,...)

# Entities info
ANGEL_SPEED = 35													# Angel speed (in case per second)
ANGEL_SPRITE_DURATION = 0.5											# Duration of each angel sprite (in second)

BEAN_FREQUENCY = 2													# Bean spawn frequency (the value increases with the score) (in second)
BEAN_SPEED = 1.8													# Bean speed (in case per second)
BEAN_SPRITE_DURATION = 0.2											# Duration of each bean sprite (in second)

LEAF_SPRITE_DURATION = 0.2											# Duration of each leaf sprite (in second)
LEAF_SPEED = 1.5													# Leaf speed (in case per second)
LEAF_WIND_SPEED = 15												# Wind force applied to bean leaf when shot (in case per second)

PYORO_EATING_DURATION = 0.04										# Duration of each pyoro eating sprite (in second)
PYORO_DIE_SPEED = 2													# Pyoro speed when it dies (in case per second)
PYORO_NOTCH_DURATION = 0.01											# Pyoro notch duration (in second)
PYORO_SHOOT_SPRITE_DURATION = 0.1									# Sprite frequency when pyoro 2 shoot (in second)
PYORO_SPEED = 25													# Pyoro speed (in case per second)

SEED_SPEED = 45														# Seed speed (in case per second)

SMOKE_SPRITE_DURATION = 0.2											# Duration of each smoke sprite (in second)

SCORE_TEXT_BLINK_DURATION = 0.05									# Duration of each text sprite (in second)
SCORE_TEXT_LIFE_DURATION = 0.3										# Time before the destruction of each text sprite (in second)

TONG_SPEED = 25														# Pyoro tong speed (in case per second)

# Default options used at first boot and when reset
DEFAULT_OPTIONS = {
	"keyboard": {
		"right": 100,
		"left": 97,
		"action": 32,
		"pause": 27
	},
	"joystick": {
		"right": {
			"inputType": 9,
			"hatId": 0,
			"value": (1, 0)
		},
		"left": {
			"inputType": 9,
			"hatId": 0,
			"value": (-1, 0)
		},
		"action": {
			"inputType": 10,
			"buttonId": 2
		},
		"pause": {
			"inputType": 10,
			"buttonId": 9
		}
	},
	"last game": 0,
	"high score": [
		0,
		0
	],
	"last game": 0,
	"music volume": 1,
	"sound volume": 1
}