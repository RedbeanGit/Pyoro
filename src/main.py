#!/usr/bin/env python3

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
from game.debug_logger import DebugLogger
from game.mod import Mod
from game.util import Errors, Game, leave_game, load_config
from gui.window import Window


def main():
    """
    Main function of the game. Must be called first except for updating.
    """

    logging.info("[main] Starting Pyoro")

    try:
        pygame.init()
        Game.options = load_config()
        Game.audio_player = AudioPlayer()
        Game.window = Window()
        Game.window.create_root_surface()
        Game.window.set_splash_render()

        Mod.load_mods()
        Mod.init_mods(Game.window)
        loop()
    except Exception:
        print("[FATAL ERROR] [loop] An unknown error occurred while starting !")
        leave_game(Errors.BOOT_ERROR)


def update():
    """
    Launch update installation.
    """

    try:
        print("[INFO] [main] Starting Debug_logger")
        Game.debug_logger = DebugLogger()
        print("[INFO] [update] Starting Pyoro v1.1 to update")

        pygame.init()

        Game.window = Window()
        Game.window.create_root_surface()
        Game.window.set_splash_render("update")
    except Exception:
        print("[FATAL ERROR] [update] An unknown error" + " occurred while updating!")
        leave_game(Errors.UPDATE_ERROR)


def loop():
    """
    Create an infinite loop and update game components.
    """

    print("[INFO] [startLoop] Starting new game loop")
    clock = pygame.time.Clock()
    tick = 0
    total_time = 0

    while True:
        try:
            pygame.event.pump()
            delta_time = clock.tick() / 1000

            Game.window.update(delta_time)
            Mod.update_mods(Game.window, delta_time)

            tick += 1
            total_time += delta_time
        except Exception:
            print(
                "[FATAL ERROR] [loop] An unknown error "
                + f"occurred! tick={tick} total_time=%{total_time}s"
            )
            leave_game(Errors.LOOP_ERROR)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    if len(sys.argv) > 1:
        if sys.argv[1] == "update":
            update()
        else:
            print(f"[WARNING] [GLOBAL] unknown argument {sys.argv[1]}")
            if len(sys.argv) > 2:
                if sys.argv[2] == "update":
                    update()
                else:
                    print(f"[WARNING] [GLOBAL] unknown argument {sys.argv[2]}")
                    main()
            else:
                main()
    else:
        main()
