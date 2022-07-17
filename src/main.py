#!/usr/bin/env python3

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
Main module and functions of Pyoro.

Created on 17/03/2018
"""

import os
import logging
import sys
import pygame

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from audio.audio_player import AudioPlayer
from game import Game
from game.mod import Mod
from game.util import loadOptions
from game.config import VERSION
from gui.window import Window


def main():
    """
    Main function of the game. Must be called first except for updating.
    """

    logging.info('[main] Starting Pyoro')

    try:
        pygame.init()
        options = loadOptions()
        Game.audioPlayer = Audio_player()
        Game.window = Window()
        Game.window.createRootSurface()
        Game.window.setSplashRender()

        Mod.loadMods()
        Mod.initMods(Game.window)
        loop()
    except Exception:
        print("[FATAL ERROR] [loop] An unknown error" \
            + " occurred while starting !")
        leaveGame(Errors.BOOT_ERROR)


def update():
    """
    Launch update installation.
    """

    try:
        print("[INFO] [main] Starting Debug_logger")
        Game.debugLogger = Debug_logger()
        print("[INFO] [update] Starting Pyoro v1.1 to update")

        pygame.init()

        Game.window = Window()
        Game.window.createRootSurface()
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
            leaveGame(Errors.LOOP_ERROR)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
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
