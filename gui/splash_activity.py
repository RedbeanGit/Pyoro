# -*- coding:utf-8 -*-

"""
Provide a splash activity while the game is booting.
"""
"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 29/10/2018
	@version: 1.1
=========================
"""

from game.config import WIDTH, HEIGHT, SPLASH_ANIMATION_DURATION, \
	ENTITIES_IMAGE_PATH
from game.update import getConnectionStream, getUpdates, downloadUpdate, \
	installUpdate
from game.util import adminRestart, restart

from gui.activity import Activity
from gui.dialog_menu import Dialog_menu
from gui.image_transformer import Image_transformer
from gui.text import Text

__author__ = "Julien Dubois"
__version__ = "1.1"

import os
import threading


class Splash_activity(Activity):

	def __init__(self, window):
		Activity.__init__(self, window)

	def initImages(self):
		path = os.path.join(ENTITIES_IMAGE_PATH, "pyoro 1", "pyoro_0_normal_1.png")
		self.window.initImage(path)
		self.images["pyoro"] = Image_transformer.resize(self.window.getImage(path), (WIDTH * 0.25, HEIGHT * 0.25))

	def initWidgets(self):
		self.addWidget("infoText", Text, (int(WIDTH * 0.5), int(HEIGHT * 0.7)), "Chargement...", anchor = (0, -1))

	def update(self, deltaTime):
		self.window.drawImage(self.images["pyoro"], (int(WIDTH * 0.375), int(HEIGHT * 0.375)))
		Activity.update(self, deltaTime)

	def setInfo(self, msg):
		self.widgets["infoText"].text = msg
		self.window.update(0)

	def waitLoading(self):
		self.setInfo("Chargement des images...")
		self.window.initImages()
		self.setInfo("Chargement des sons...")
		self.window.initAudioPlayer()
		self.setInfo("Initialisation des manettes...")
		self.window.initJoysticks()
		self.setInfo("Recherche des mises à jour...")
		self.searchForUpdates()

	def searchForUpdates(self):
		ftpMgr = getConnectionStream()

		if ftpMgr:
			newVersions = getUpdates(ftpMgr)
			if newVersions:
				self.addWidget("askForUpdateDialogMenu", Dialog_menu, (int(WIDTH * 0.5), int(HEIGHT * 0.5)), "Mettre à jour ?", self.downloadUpdate, positiveArgs = (ftpMgr, newVersions), negativeFct = self.window.setMenuRender, anchor = (0, 0), description = "Des mises à jours sont disponibles")
			else:
				print("[INFO] [Splash_activity.searchForUpdates] No update available")
				self.window.setMenuRender()
		else:
			print("[INFO] [Splash_activity.searchForUpdates] Unable to detect new updates")
			self.window.setMenuRender()

	def downloadUpdate(self, ftpMgr, newVersions):
		for key, newVersion in enumerate(newVersions):
			self.setInfo("Téléchargement de la mise à jour %s (%s/%s)" % (newVersion, key, len(newVersions)))
			if not downloadUpdate(ftpMgr, newVersion):
				self.addWidget("updateFailedDialogMenu", Dialog_menu, (int(WIDTH * 0.5), int(HEIGHT * 0.5)), "La mise à jour a échoué !", self.window.setMenuRender, anchor = (0, 0), description = "Réessayez plus tard !")
			else:
				self.addWidget("updateSuccessDialogMenu", Dialog_menu, (int(WIDTH * 0.5), int(HEIGHT * 0.5)), "Mises à jour téléchargées !", adminRestart, positiveArgs = ("update",), anchor = (0, 0), description = "Les mises à jour vont être installées")
		self.setInfo("Téléchargements terminés !")
		ftpMgr.disconnect()

	def installUpdate(self):
		self.setInfo("Installation des mises à jour...")
		installUpdate()
		restart()