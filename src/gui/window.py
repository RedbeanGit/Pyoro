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

from audio.audio_player import Audio_player
from game.config import NAME, GUI_IMAGE_PATH, CASE_SIZE, WINDOW_COLOR
from game.util import loadOptions, saveOptions, getResourcePaths, \
	leaveGame, Game, Errors
from gui.level_activity import Level_activity
from gui.menu_activity import Menu_activity
from gui.splash_activity import Splash_activity


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
		self.rootSurface = None
		self.activity = None

	def createRootSurface(self):
		"""
		Create a pygame window in fullscreen mode.
		"""

		print("[INFO] [Window.createRootSurface] Creating new Pygame window " \
			+ "in fullscreen mode with auto definition")

		iconPath = os.path.join(GUI_IMAGE_PATH, "pyoro_icon.png")
		self.rootSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE)
		pygame.display.set_caption(NAME)

		if os.path.exists(iconPath):
			try:
				pygame.display.set_icon(pygame.image.load(
					iconPath).convert_alpha())
			except Exception:
				print("[FATAL ERROR] [Window.createRootSurface] Unable to load" \
					+ " the window icon")
				leaveGame(Errors.BAD_RESOURCE)
		else:
			print("[WARNING] [Window.createRootSurface] Window icon not found")

	def loadJoysticks(self):
		"""
		Initialize all connected joysticks.
		"""

		print("[INFO] [Window.initJoysticks] Initializing joystick inputs")
		self.joysticks.clear()
		for i in range(pygame.joystick.get_count()):
			joystick = pygame.joystick.Joystick(i)
			joystick.init()
			self.joysticks.append(joystick)

	def loadImages(self):
		"""
		Load all images to the RAM.
		"""

		print("[INFO] [Window.initImages] Loading images to RAM memory")
		self.images["unknown"] = self.createRemplacementImage()
		imagePaths = getResourcePaths("images")
		for imagePath in imagePaths:
			image = os.path.join("data", *imagePath)
			self.loadImage(image)

	def loadImage(self, imagePath):
		"""
		Load an image to the RAM.

		:type imagePath: str
		:param imagePath: The filepath of the image to load.
		"""

		if os.path.exists(imagePath):
			self.images[imagePath] = pygame.image.load(imagePath)
		else:
			print("[WARNING] [Window.initImage] Unable" \
				+ ' to find "%s"' % imagePath)

	def createRemplacementImage(self):
		"""
		Create a replacement image and return it.

		:rtype: pygame.surface.Surface
		:returns: A purple and black image.
		"""

		print("[INFO] [Window.createRemplacementImage] Creating the replacement image")
		image = pygame.Surface((16, 16))
		image.fill((255, 0, 255), (0, 0, 8, 8))
		image.fill((255, 0, 255), (8, 8, 8, 8))
		return image

	def getImage(self, imagePath, alphaChannel=True):
		"""
		Get a copy of a loaded image. If the searched image hasn't been
		loaded, return a replacement image.

		:type imagePath: str
		:param imagePath: The filepath to the image to get.

		:type alphaChannel: bool
		:param alphaChannel: (Optional) If True, return an image with an
			alpha channel that can't be modified; otherwise, return an image
			fully opaque but alpha can be modified.

		:rtype: pygame.surface.Surface
		:returns: A loaded or replacement image.
		"""

		if imagePath in self.images:
			if alphaChannel:
				return self.images[imagePath].convert_alpha()
			return self.images[imagePath].convert()

		print('[WARNING] [Window.getImage] Image "%s" ' % filepath \
			+ "not loaded! Using a remplacement image")

		if alphaChannel:
			return self.images["unknown"].convert()
		return self.images["unknown"].convert_alpha()

	def updateEvents(self):
		"""
		Update the activity with the current events in the pygame event buffer.
		"""

		for event in pygame.event.get():
			if event.type == QUIT:
				self.destroy()
			elif event.type == K_F4 and pygame.key.get_mods() in (K_RALT, K_LALT):
				self.destroy()
			elif self.activity:
				self.activity.updateEvent(event)

	def update(self, deltaTime):
		"""
		Update the current level and all graphical components.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last update (in seconds).
		"""

		self.updateEvents()

		if self.activity:
			self.activity.update(deltaTime)
		pygame.display.update()

	def destroy(self):
		"""
		Destroy the current activity and leave the game.
		"""

		print("[INFO] [Window.destroy] Destroying window")
		self.destroyActivity()
		leaveGame()

	def destroyActivity(self):
		"""
		Destroy the current activity and stop sounds and musics.
		"""

		if self.activity:
			print("[INFO] [Window.destroyActivity] Destroying " \
				+ "the current activity")
			self.activity.destroy()
			Game.audioPlayer.stopAudio()
		else:
			print("[INFO] [Window.destroyActivity] No current activity")

	def setSplashRender(self, bootOption = "default"):
		"""
		Replace the current activity by a new
		gui.splash_activity.Splash_activity.

		:type bootOption: str
		:param bootOption: (Optional) An option for alternate starts. It can be
			"default" (default option) or "update".

		:Example: myWindow.setSplashRender("update") will
			show an update installation dialog.
		"""

		self.destroyActivity()
		print("[INFO] [Window.setSplashRender] Creating splash activity " \
			+ "with bootOption=%s" % bootOption)
		self.activity = Splash_activity(self)

		if bootOption == "update":
			self.activity.bootUpdate()
		elif bootOption == "default":
			self.activity.boot()
		else:
			print("[FATAL ERROR] [Window.setSplashRender] Unknown boot option" \
				+ " '%s'" % bootOption)
			leaveGame(Errors.CODE_ERROR)

	def setMenuRender(self):
		"""
		Replace the current activity by a new
		gui.menu_activity.Menu_activity.
		"""

		self.destroyActivity()
		gameId = Game.options.get("last game", 0)

		if gameId not in (0, 1):
			print("[FATAL ERROR] [Window.setMenuRender]" \
				+ " Unknown gameId %s" % gameId)
			leaveGame(Errors.BAD_RESOURCE)

		print("[INFO] [Window.setMenuRender] Creating menu" \
			+ " activity with gameId=%s" % gameId)
		self.activity = Menu_activity(self, gameId)

	def setGameRender(self, gameId = 0):
		"""
		Replace the current activity by a new
		gui.level_activity.Level_activity.

		:type gameId: int
		:param gameId: An id representing the game to load.
			0 = Pyoro
			1 = Pyoro 2
		"""

		if gameId in (0, 1):
			self.destroyActivity()
			print("[INFO] [Window.setMenuRender] Creating level" \
				+ " activity with gameId=%s" % gameId)
			self.activity = Level_activity(self, gameId)
		else:
			print("[FATAL ERROR] [Window.setGameRender]" \
				+ " Unknown gameId %s" % gameId)
			leaveGame(Errors.CODE_ERROR)

	def drawImage(self, image, pos):
		"""
		Draw an image on the screen.

		:type image: pygame.surface.Surface
		:param image: The surface to draw on the screen.

		:type pos: tuple<int>
		:param pos: The (x, y) position of the surface on the screen.
			(0, 0) = the top left corner of the screen.
		"""

		if self.rootSurface:
			self.rootSurface.blit(image, pos)
		else:
			print("[WARNING] [Window.drawImage] No root surface to draw on")

	def getSize(self):
		"""
		Return the size of the game window.

		:rtype: tuple
		:returns: A (width, height) tuple.
		"""
		
		if self.rootSurface:
			return self.rootSurface.get_size()
		else:
			print("[WARNING] [Window.getSize] Non root surface")
