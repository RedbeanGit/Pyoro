# -*- coding: utf-8 -*-

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
Provide a class to manage the game window.

Created on 18/03/2018
"""

import os
import pygame
from pygame.locals import QUIT, K_F4, K_RALT, K_LALT

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import NAME, GUI_IMAGE_PATH
from game.util import get_resource_paths, leave_game, Game, Errors
from gui.level_activity import LevelActivity
from gui.menu_activity import MenuActivity
from gui.splash_activity import SplashActivity


class Window:
    """
    Main game window, manage the levels and all graphical components.
    """

    def __init__(self):
        """
        Initialize a new Window.
        """

        self.images = {}
        self.joysticks = []
        self.root_surface = None
        self.activity = None

    def create_root_surface(self):
        """
        Create a pygame window in fullscreen mode.
        """

        print("[INFO] [Window.create_root_surface] Creating new Pygame window "
              + "in fullscreen mode with auto definition")

        icon_path = os.path.join(GUI_IMAGE_PATH, "pyoro_icon.png")
        self.root_surface = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN | pygame.HWSURFACE)
        pygame.display.set_caption(NAME)

        if os.path.exists(icon_path):
            try:
                pygame.display.set_icon(pygame.image.load(
                    icon_path).convert_alpha())
            except Exception:
                print("[FATAL ERROR] [Window.create_root_surface] Unable to load"
                      + " the window icon")
                leave_game(Errors.BAD_RESOURCE)
        else:
            print("[WARNING] [Window.create_root_surface] Window icon not found")

    def load_joysticks(self):
        """
        Initialize all connected joysticks.
        """

        print("[INFO] [Window.initJoysticks] Initializing joystick inputs")
        self.joysticks.clear()
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)

    def load_images(self):
        """
        Load all images to the RAM.
        """

        print("[INFO] [Window.initImages] Loading images to RAM memory")
        self.images["unknown"] = self.create_remplacement_image()
        image_paths = get_resource_paths("images")
        for image_path in image_paths:
            image = os.path.join("data", *image_path)
            self.load_image(image)

    def load_image(self, image_path):
        """
        Load an image to the RAM.

        :type image_path: str
        :param image_path: The filepath of the image to load.
        """

        if os.path.exists(image_path):
            self.images[image_path] = pygame.image.load(image_path)
        else:
            print(
                f"[WARNING] [Window.initImage] Unable to find '{image_path}'")

    def create_remplacement_image(self):
        """
        Create a replacement image and return it.

        :rtype: pygame.surface.Surface
        :returns: A purple and black image.
        """

        print("[INFO] [Window.create_remplacement_image] Creating the replacement image")
        image = pygame.Surface((16, 16))
        image.fill((255, 0, 255), (0, 0, 8, 8))
        image.fill((255, 0, 255), (8, 8, 8, 8))
        return image

    def get_image(self, image_path, alpha_channel=True):
        """
        Get a copy of a loaded image. If the searched image hasn't been
        loaded, return a replacement image.

        :type image_path: str
        :param image_path: The filepath to the image to get.

        :type alpha_channel: bool
        :param alpha_channel: (Optional) If True, return an image with an
            alpha channel that can't be modified; otherwise, return an image
            fully opaque but alpha can be modified.

        :rtype: pygame.surface.Surface
        :returns: A loaded or replacement image.
        """

        if image_path in self.images:
            if alpha_channel:
                return self.images[image_path].convert_alpha()
            return self.images[image_path].convert()

        print(
            f'[WARNING] [Window.get_image] Image "{image_path}"'
            + ' not loaded! Using a remplacement image')

        if alpha_channel:
            return self.images["unknown"].convert()
        return self.images["unknown"].convert_alpha()

    def update_events(self):
        """
        Update the activity with the current events in the pygame event buffer.
        """

        for event in pygame.event.get():
            if event.type == QUIT:
                self.destroy()
            elif event.type == K_F4 and pygame.key.get_mods() in (K_RALT, K_LALT):
                self.destroy()
            elif self.activity:
                self.activity.update_event(event)

    def update(self, delta_time):
        """
        Update the current level and all graphical components.

        :type delta_time: float
        :param delta_time: Time elapsed since the last update (in seconds).
        """

        self.update_events()

        if self.activity:
            self.activity.update(delta_time)
        pygame.display.update()

    def destroy(self):
        """
        Destroy the current activity and leave the game.
        """

        print("[INFO] [Window.destroy] Destroying window")
        self.destroy_activity()
        leave_game()

    def destroy_activity(self):
        """
        Destroy the current activity and stop sounds and musics.
        """

        if self.activity:
            print("[INFO] [Window.destroy_activity] Destroying "
                  + "the current activity")
            self.activity.destroy()
            Game.audio_player.stop_audio()
        else:
            print("[INFO] [Window.destroy_activity] No current activity")

    def set_splash_render(self, boot_option="default"):
        """
        Replace the current activity by a new
        gui.splashActivity.SplashActivity.

        :type boot_option: str
        :param boot_option: (Optional) An option for alternate starts. It can be
            "default" (default option) or "update".

        :Example: myWindow.set_splash_render("update") will
            show an update installation dialog.
        """

        self.destroy_activity()
        print("[INFO] [Window.set_splash_render] Creating splash activity "
              + f"with boot_option={boot_option}")
        self.activity = SplashActivity(self)

        if boot_option == "update":
            self.activity.boot_update()
        elif boot_option == "default":
            self.activity.boot()
        else:
            print(
                "[FATAL ERROR] [Window.set_splash_render] Unknown boot option '{boot_option}'")
            leave_game(Errors.CODE_ERROR)

    def set_menu_render(self):
        """
        Replace the current activity by a new
        gui.menuActivity.MenuActivity.
        """

        self.destroy_activity()
        game_id = Game.options.get("last game", 0)

        if game_id not in (0, 1):
            print(
                f"[FATAL ERROR] [Window.set_menu_render] Unknown game_id {game_id}")
            leave_game(Errors.BAD_RESOURCE)

        print(
            f"[INFO] [Window.set_menu_render] Creating menu activity with game_id={game_id}")
        self.activity = MenuActivity(self, game_id)

    def set_game_render(self, game_id=0):
        """
        Replace the current activity by a new
        gui.levelActivity.LevelActivity.

        :type game_id: int
        :param game_id: An id representing the game to load.
            0 = Pyoro
            1 = Pyoro 2
        """

        if game_id in (0, 1):
            self.destroy_activity()
            print(
                f"[INFO] [Window.set_menu_render] Creating level activity with game_id={game_id}")
            self.activity = LevelActivity(self, game_id)
        else:
            print(
                f"[FATAL ERROR] [Window.set_game_render] Unknown game_id {game_id}")
            leave_game(Errors.CODE_ERROR)

    def draw_image(self, image, pos):
        """
        Draw an image on the screen.

        :type image: pygame.surface.Surface
        :param image: The surface to draw on the screen.

        :type pos: tuple<int>
        :param pos: The (x, y) position of the surface on the screen.
            (0, 0) = the top left corner of the screen.
        """

        if self.root_surface:
            self.root_surface.blit(image, pos)
        else:
            print("[WARNING] [Window.draw_image] No root surface to draw on")

    def get_size(self):
        """
        Return the size of the game window.

        :rtype: tuple
        :returns: A (width, height) tuple.
        """

        if self.root_surface:
            return self.root_surface.get_size()
        else:
            print("[WARNING] [Window.get_size] Non root surface")
