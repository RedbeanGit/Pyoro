# -*- coding: utf-8 -*-

# 	This file is part of Pyoro (A Python fan game).
#
# 	Metawars is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	Metawars is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
Provide useful constants used in the game.

Created on 17/03/2018
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"


# General information about the game
# Debugging mode (if you want to see logs in a console)
DEBUG = True
# frame per seconds
FPS = 60
# game name
NAME = "PYORO"
# game version
VERSION = "1.1.1"
# background color
WINDOW_COLOR = (120, 120, 120)
# If True, use less resources but cannot read several sounds at the same time
LOW_AUDIO = True

# Update server address and login
# FTP host
UPDATE_HOST = "ftpupload.net"
# FTP username
UPDATE_USER = "epiz_22757918"
# FTP password
UPDATE_PASSWORD = "6UJDteWTmclaL"

# Some level constants
# Air resistance value for leaf and seeds wind effect
AIR_RESISTANCE = 25
# Speed of transition between to backgrounds
BACKGROUND_TRANSITION_DURATION = 3
# Size of a block (in mm)
CASE_SIZE = 10
# Gravity force for seeds falling effect
GRAVITY_FORCE = 9.81
# Acceleration of the level speed each second
SPEED_ACCELERATION = 0.01
# Duration of each animated background
BACKGROUND_ANIMATED_DURATION = 1
# (for last backgrounds)
# Duration of each animation during splash screen (currently useless)
SPLASH_ANIMATION_DURATION = 0.125

# Main file paths
# File path to Graphical User Interface images
GUI_IMAGE_PATH = os.path.join("data", "images", "gui")
# File path to entities images
ENTITIES_IMAGE_PATH = os.path.join("data", "images", "entities")
# File path to level images (backgrounds, blocks,...)
LEVEL_IMAGE_PATH = os.path.join("data", "images", "level")

# Entities info
# Angel speed (in case per second)
ANGEL_SPEED = 35
# Duration of each angel sprite (in second)
ANGEL_SPRITE_DURATION = 0.5

# Bean spawn frequency (the value increases with the score) (in second)
BEAN_FREQUENCY = 2
# Bean speed (in case per second)
BEAN_SPEED = 1.8
# Duration of each bean sprite (in second)
BEAN_SPRITE_DURATION = 0.2

# Duration of each leaf sprite (in second)
LEAF_SPRITE_DURATION = 0.2
# Leaf speed (in case per second)
LEAF_SPEED = 1.5
# Wind force applied to bean leaf when shot (in case per second)
LEAF_WIND_SPEED = 15

# Duration of each pyoro eating sprite (in second)
PYORO_EATING_DURATION = 0.04
# Pyoro speed when it dies (in case per second)
PYORO_DIE_SPEED = 2
# Pyoro notch duration (in second)
PYORO_NOTCH_DURATION = 0.01
# Sprite frequency when pyoro 2 shoot (in second)
PYORO_SHOOT_SPRITE_DURATION = 0.1
# Pyoro speed (in case per second)
PYORO_SPEED = 25

# Seed speed (in case per second)
SEED_SPEED = 45

# Duration of each smoke sprite (in second)
SMOKE_SPRITE_DURATION = 0.2

# Duration of each text sprite (in second)
SCORE_TEXT_BLINK_DURATION = 0.05
# Time before the destruction of each text sprite (in second)
SCORE_TEXT_LIFE_DURATION = 0.3

# Pyoro tongue speed (in case per second)
TONG_SPEED = 25

# Default options used at first boot and when reset
DEFAULT_OPTIONS = {
    "keyboard": {"right": 100, "left": 97, "action": 32, "pause": 27},
    "joystick": {
        "right": {"input_type": 9, "hat_id": 0, "value": (1, 0)},
        "left": {"input_type": 9, "hat_id": 0, "value": (-1, 0)},
        "action": {"input_type": 10, "button_id": 2},
        "pause": {"input_type": 10, "button_id": 9},
    },
    "last game": 0,
    "high score": [0, 0],
    "music volume": 1,
    "sound volume": 1,
}
