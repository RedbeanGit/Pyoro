# -*- coding:utf-8 -*-

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
Provide a splash activity while the game is booting.

Created on 29/10/2018
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import ENTITIES_IMAGE_PATH
from game.update import (
    get_connection_stream,
    get_updates,
    download_update,
    install_update,
)
from game.util import admin_restart, restart, Game

from gui.activity import Activity
from gui.dialog_menu import DialogMenu
from gui.image_widget import ImageWidget
from gui.text import Text


class SplashActivity(Activity):
    """
    First activity launch while the game is loading resources.
    """

    def __init__(self, window):
        """
        Initialize a SplashActivity object.

        :type window: gui.window.Window
        :param window: The parent window of this activity.
        """

        Activity.__init__(self, window)

    def init_widgets(self):
        """
        Load a text widget which will be used to display loading messages.
        """

        # Loading text size, position and anchor position
        pos = self.layout.get_widget_pos("splash_image")
        size = self.layout.get_widget_size("splash_image")
        anchor = self.layout.get_widget_anchor("splash_image")
        path = os.path.join(ENTITIES_IMAGE_PATH, "pyoro 1", "pyoro_0_normal_1.png")

        # Creating the text widget
        self.window.load_image(path)
        self.add_widget(
            "splash_image", ImageWidget, pos, path, size=size, anchor=anchor
        )

        # Loading text size, position and anchor position
        pos = self.layout.get_widget_pos("splash_text")
        size = self.layout.get_font_size("splash_text")
        anchor = self.layout.get_widget_anchor("splash_text")

        # Creating the text widget
        self.add_widget(
            "splash_text", Text, pos, "Chargement...", font_size=size, anchor=anchor
        )

    def set_info(self, msg):
        """
        Change the message currently displayed and update the screen.

        :type msg: str
        :param msg: The messaege to display.
        """

        self.widgets["splash_text"].text = msg
        # It's important to update the window otherwise the message will not
        # be showed
        self.window.update(0)

    def boot(self):
        """
        Load game resources, search for updates and display messages about the
        current loading. This method should be called only once when the game
        start.
        """

        self.set_info("Chargement des images...")
        self.window.load_images()
        self.set_info("Chargement des sons...")
        Game.audio_player.load_audio()
        Game.audio_player.sound_volume = Game.options.get("sound volume", 1)
        Game.audio_player.music_volume = Game.options.get("music volume", 1)
        Game.audio_player.start()
        self.set_info("Initialisation des manettes...")
        self.window.load_joysticks()
        self.set_info("Recherche des mises à jour...")
        self.search_for_updates()

    def search_for_updates(self):
        """
        Search for updates. If an update is available, display a dialog to ask
        the user if he wants to install it.
        """

        ftp_mgr = get_connection_stream()

        if ftp_mgr:
            new_versions = get_updates(ftp_mgr)
            if new_versions:

                # Loading dialog size, position and anchor position
                size = self.layout.get_widget_size("ask_for_update_dialog")
                pos = self.layout.get_widget_pos("ask_for_update_dialog")
                anchor = self.layout.get_widget_anchor("ask_for_update_dialog")

                self.add_widget(
                    "ask_for_update_dialog",
                    DialogMenu,
                    pos,
                    "Mettre à jour ?",
                    self.download_update,
                    size=size,
                    anchor=anchor,
                    positive_args=(ftp_mgr, new_versions),
                    negative_fct=self.window.set_menu_render,
                    description="Des mises à jours sont disponibles",
                )
            else:
                print("[INFO] [SplashActivity.search_for_updates] No update available")
                self.window.set_menu_render()
        else:
            print(
                "[INFO] [SplashActivity.search_for_updates] Unable"
                + " to detect new updates"
            )
            self.window.set_menu_render()

    def download_update(self, ftp_mgr, new_versions):
        """
        Begin to download updates and display a loading message. Once finished,
        display a dialog about the installation status (success or fail).
        """

        success = True

        for key, new_version in enumerate(new_versions):
            self.set_info(
                f"Téléchargement de la mise à jour {new_version} ({key}/{len(new_versions)})"
            )

            # If something wrong happen, stop downloading
            if not download_update(ftp_mgr, new_version):
                # Loading widget size, position and anchor position
                size = self.layout.get_widget_size("update_failed_dialog")
                pos = self.layout.get_widget_pos("update_failed_dialog")
                anchor = self.layout.get_widget_anchor("update_failed_dialog")

                self.add_widget(
                    "update_failed_dialog",
                    DialogMenu,
                    pos,
                    "La mise à jour a échoué !",
                    self.window.set_menu_render,
                    size=size,
                    anchor=anchor,
                    description="Réessayez plus tard !",
                )
                success = False

        if success:
            # Loading widget size, position and anchor position
            size = self.layout.get_widget_size("update_success_dialog")
            pos = self.layout.get_widget_pos("update_success_dialog")
            anchor = self.layout.get_widget_anchor("update_success_dialog")

            self.add_widget(
                "update_success_dialog",
                DialogMenu,
                pos,
                "Mises à jour téléchargées !",
                admin_restart,
                size=size,
                anchor=anchor,
                positive_args=("update",),
                description="Les mises à jour vont être installées",
            )

            self.set_info("Téléchargements terminés !")
        else:
            self.set_info("Erreur lors du téléchargement !")

        ftp_mgr.disconnect()

    def boot_update(self):
        """
        Install an update already downloaded and restart the game. This method
        should be used with admin or root privileges.
        """

        self.set_info("Installation des mises à jour...")
        install_update()
        restart()
