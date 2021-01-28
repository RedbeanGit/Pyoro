# -*- coding:utf-8 -*-

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
Provide a splash activity while the game is booting.

Created on 29/10/2018
"""

import os
import threading

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import SPLASH_ANIMATION_DURATION, \
	ENTITIES_IMAGE_PATH
from game.update import getConnectionStream, getUpdates, downloadUpdate, \
	installUpdate
from game.util import adminRestart, restart, Game

from gui.activity import Activity
from gui.dialog_menu import Dialog_menu
from gui.image_widget import Image_widget
from gui.text import Text


class Splash_activity(Activity):
	"""
	First activity launch while the game is loading resources.
	"""

	def __init__(self, window):
		"""
		Initialize a Splash_activity object.

		:type window: gui.window.Window
		:param window: The parent window of this activity.
		"""

		Activity.__init__(self, window)

	def initWidgets(self):
		"""
		Load a text widget which will be used to display loading messages.
		"""

		# Loading text size, position and anchor position
		pos = self.layout.getWidgetPos("splash_image")
		size = self.layout.getWidgetSize("splash_image")
		anchor = self.layout.getWidgetAnchor("splash_image")
		path = os.path.join(ENTITIES_IMAGE_PATH, "pyoro 1", "pyoro_0_normal_1.png")

		# Creating the text widget
		self.window.loadImage(path)
		self.addWidget("splash_image", Image_widget, pos, path, size = size, \
			anchor = anchor)

		# Loading text size, position and anchor position
		pos = self.layout.getWidgetPos("splash_text")
		size = self.layout.getFontSize("splash_text")
		anchor = self.layout.getWidgetAnchor("splash_text")

		# Creating the text widget
		self.addWidget("splash_text", Text, pos, "Chargement...", \
			fontSize = size, anchor = anchor)

	def setInfo(self, msg):
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

		self.setInfo("Chargement des images...")
		self.window.loadImages()
		self.setInfo("Chargement des sons...")
		Game.audioPlayer.loadAudio()
		Game.audioPlayer.soundVolume = Game.options.get("sound volume", 1)
		Game.audioPlayer.musicVolume = Game.options.get("music volume", 1)
		Game.audioPlayer.start()
		self.setInfo("Initialisation des manettes...")
		self.window.loadJoysticks()
		self.setInfo("Recherche des mises à jour...")
		self.searchForUpdates()

	def searchForUpdates(self):
		"""
		Search for updates. If an update is available, display a dialog to ask
		the user if he wants to install it.
		"""

		ftpMgr = getConnectionStream()

		if ftpMgr:
			newVersions = getUpdates(ftpMgr)
			if newVersions:

				# Loading dialog size, position and anchor position
				size = self.layout.getWidgetSize("ask_for_update_dialog")
				pos = self.layout.getWidgetPos("ask_for_update_dialog")
				anchor = self.layout.getWidgetAnchor("ask_for_update_dialog")

				self.addWidget("ask_for_update_dialog", Dialog_menu, \
					pos, "Mettre à jour ?", self.downloadUpdate, \
					size = size, anchor = anchor, \
					positiveArgs = (ftpMgr, newVersions), \
					negativeFct = self.window.setMenuRender, \
					description = "Des mises à jours sont disponibles")
			else:
				print("[INFO] [Splash_activity.searchForUpdates] No update available")
				self.window.setMenuRender()
		else:
			print("[INFO] [Splash_activity.searchForUpdates] Unable" \
				+ " to detect new updates")
			self.window.setMenuRender()

	def downloadUpdate(self, ftpMgr, newVersions):
		"""
		Begin to download updates and display a loading message. Once finished,
		display a dialog about the installation status (success or fail).
		"""

		success = True

		for key, newVersion in enumerate(newVersions):
			self.setInfo("Téléchargement de la " \
				+ "mise à jour %s (%s/%s)" % (newVersion, key, len(newVersions)))

			# If something wrong happen, stop downloading
			if not downloadUpdate(ftpMgr, newVersion):
				# Loading widget size, position and anchor position
				size = self.layout.getWidgetSize("update_failed_dialog")
				pos = self.layout.getWidgetPos("update_failed_dialog")
				anchor = self.layout.getWidgetAnchor("update_failed_dialog")

				self.addWidget("update_failed_dialog", Dialog_menu, \
					pos, "La mise à jour a échoué !", \
					self.window.setMenuRender, size = size, anchor = anchor, \
					description = "Réessayez plus tard !")
				success = False

		if success:
			# Loading widget size, position and anchor position
			size = self.layout.getWidgetSize("update_success_dialog")
			pos = self.layout.getWidgetPos("update_success_dialog")
			anchor = self.layout.getWidgetAnchor("update_success_dialog")

			self.addWidget("update_success_dialog", Dialog_menu, \
				pos, "Mises à jour téléchargées !", adminRestart, \
				size = size, anchor = anchor, positiveArgs = ("update",), \
				description = "Les mises à jour vont être installées")

			self.setInfo("Téléchargements terminés !")
		else:
			self.setInfo("Erreur lors du téléchargement !")

		ftpMgr.disconnect()

	def bootUpdate(self):
		"""
		Install an update already downloaded and restart the game. This method
		should be used with admin or root privileges.
		"""

		self.setInfo("Installation des mises à jour...")
		installUpdate()
		restart()
