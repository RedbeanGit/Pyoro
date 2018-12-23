#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main module and functions of Pyoro.

Created on 17/03/2018
"""

from audio.audio_player import Audio_player
from game.debug_logger import Debug_logger
from game.mod import Mod
from game.util import checkData, checkModules, Errors, Game, leaveGame
from gui.window import Window

__author__ = "Julien Dubois"
__version__ = "1.1"

import os
import sys
import traceback
import pygame


def main():
	"""
	Main function of the game. Must be called first except for updating.
	"""

	try:
		Game.debugLogger = Debug_logger()
		print("[INFO] [main] Starting Pyoro v1.1")

		if not checkModules():
			print("[FATAL ERROR] [main] Module not found !")
			leaveGame(Errors.MODULE_NOT_FOUND)

		if not checkData():
			print("[FATAL ERROR] [main] No data found !")
			leaveGame(Errors.DATA_NOT_FOUND)

		Game.audioPlayer = Audio_player()

		Game.window = Window()
		Game.window.loadImages()
		Game.window.setSplashRender()

		Mod.loadMods()
		Mod.initMods(Game.window)
		loop()
	except Exception:
		print("[FATAL ERROR] [loop] An unknown error" \
			+ " occurred while starting !")
		print(traceback.format_exc())
		leaveGame(Errors.BOOT_ERROR)


def update():
	"""
	Launch update installation.
	"""

	try:
		Game.debugLogger = Debug_logger()
		print("[INFO] [update] Starting Pyoro v1.1 to update")

		Game.window = Window()
		Game.window.loadImages()
		Game.window.setSplashRender("update")
	except Exception:
		print("[FATAL ERROR] [update] An unknown error" \
			+ " occurred while updating!")
		leaveGame(Errors.UPDATE_ERROR)


def loop():
	"""
	Create an infinite loop and update game components.
	"""

	print("[INFO] [startLoop] Starting new game loop")
	clock = pygame.time.Clock()
	tick = 0
	totalTime = 0

	while True:
		try:
			pygame.event.pump()
			deltaTime = clock.tick() / 1000
			
			Game.window.update(deltaTime)
			Mod.updateMods(Game.window, deltaTime)
			
			tick += 1
			totalTime += deltaTime
		except Exception:
			print("[FATAL ERROR] [loop] An unknown error " \
				+ "occurred! tick=%s totalTime=%ss" % (tick, totalTime))
			print(traceback.format_exc())
			leaveGame(Errors.LOOP_ERROR)

if __name__ == "__main__":
	if len(sys.argv) > 1: 
		if sys.argv[1] == "update":
			update()
		else:
			print("[WARNING] [GLOBAL] unknown" \
				+ " argument %s" % sys.argv[1])
			if len(sys.argv) > 2:
				if sys.argv[2] == "update":
					update()
				else:
					print("[WARNING] [GLOBAL] unknown" \
					+ " argument %s" % sys.argv[2])
					main()
			else:
				main()
	else:
		main()