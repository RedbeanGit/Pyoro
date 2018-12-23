# -*- coding: utf-8 -*-

"""
Provide a class to manage the game window.

Created on 18/03/2018
"""

from audio.audio_player import Audio_player
from game.config import WIDTH, HEIGHT, NAME, GUI_IMAGE_PATH, CASE_SIZE
from game.util import loadOptions, saveOptions, getResourcePaths, \
	leaveGame, Game
from gui.image_transformer import Image_transformer
from gui.level_activity import Level_activity
from gui.menu_activity import Menu_activity
from gui.splash_activity import Splash_activity

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import os
import pygame
from pygame.locals import QUIT

class Window:
	"""
	Main game window, manage the levels and all graphical.
	"""

	def __init__(self):
		"""
		Initialize a new Window.
		"""

		self.images = {}
		self.joysticks = []
		self.root_window = None

		self.initPygameWindow()

		self.options = loadOptions()
		self.activity = None
		self.frame = None

	def initPygameWindow(self):
		"""
		Create a pygame window with a defined definition, title and icon.
		"""

		print("[INFO] [Window.initPygameWindow] Creating new Pygame window " \
			+ "with definition %sx%s" % (WIDTH + 10, HEIGHT + 10))
		pygame.init()

		w, h = self.getScreenSize()
		w = int(w * 0.6 - (w * 0.6) % CASE_SIZE)
		h = int(h * 0.6 - (h * 0.6) % CASE_SIZE)
		s = min(w, h)
		self.root_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		pygame.display.set_caption(NAME)
		iconPath = os.path.join(GUI_IMAGE_PATH, "pyoro_icon.png")
		try:
			pygame.display.set_icon(pygame.image.load(
				iconPath).convert_alpha())
		except pygame.error:
			print("[WARNING] [Window.initPygameWindow] Unable to load the " \
				+ 'window\'s icon "%s"' % iconPath)

	def initJoysticks(self):
		"""
		Initialize all connected joysticks.
		"""

		print("[INFO] [Window.initJoysticks] Initializing joystick inputs")
		for i in range(pygame.joystick.get_count()):
			joystick = pygame.joystick.Joystick(i)
			joystick.init()
			self.joysticks.append(joystick)

	def initImages(self):
		"""
		Load all images to the RAM.
		"""

		print("[INFO] [Window.initImages] Loading images to RAM memory")
		self.images["unknown"] = self.createRemplacementImage()
		imagePaths = getResourcePaths("images")
		for imagePath in imagePaths:
			image = os.path.join("data", *imagePath)
			self.initImage(image)

	def initImage(self, imagePath):
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

	def initAudioPlayer(self):
		"""
		Initialize the audio player.
		"""

		if Game.audioPlayer:
			Game.audioPlayer.loadAudio()
			Game.audioPlayer.start()

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

	def loadImages(self):
		w, h = self.getSize()
		self.initImage(os.path.join(GUI_IMAGE_PATH, "frame.png"))
		self.frame = Image_transformer.stretch(
			self.getImage(os.path.join(GUI_IMAGE_PATH, "frame.png")),
			(w + 10, h + 10), 5)

	def getImage(self, imagePath, alphaChannel = True):
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

	def update(self, deltaTime):
		"""
		Update the current level and all graphical components.

		:type deltaTime: float
		:param deltaTime: Elapsed time since the last update (in seconds).
		"""

		for event in pygame.event.get():
			if event.type == QUIT:
				self.destroy()
			if self.activity:
				self.activity.updateEvent(event)
		self.root_window.blit(self.frame, (0, 0))
		if self.activity:
			self.activity.update(deltaTime)
		pygame.display.update()

	def destroy(self):
		"""
		Destroy the current activity, the window, save
		the options and leave the game.
		"""

		print("[INFO] [Window.destroy] Destroying window")
		if self.activity:
			self.activity.destroy()
		saveOptions(self.options)
		leaveGame()

	def destroyActivity(self):
		"""
		Destroy the current activity and stop sounds and musics.
		"""

		if self.activity:
			print("[INFO] [Window.destroyActivity] Destroying " \
				+ "current activity")
			self.activity.destroy()
			Game.audioPlayer.stopAudio()
		else:
			print("[INFO] [Window.destroyActivity] No current activity")

	def setSplashRender(self, option = None):
		"""
		Replace the current activity by a new
		gui.splash_activity.Splash_activity.

		:type option: str
		:param option: (Optional) An option for alternate starts.

		:Example: myWindow.setSplashRender("update") will
			show an update installation dialog.
		"""

		self.destroyActivity()
		print("[INFO] [Window.setSplashRender] Creating splash activity")
		self.activity = Splash_activity(self)
		if option == "update":
			self.activity.installUpdate()
		else:
			self.activity.waitLoading()

	def setMenuRender(self):
		"""
		Replace the current activity by a new
		gui.menu_activity.Menu_activity.
		"""

		self.destroyActivity()
		gameId = self.getOption("last game")

		if gameId not in (0, 1):
			print("[WARNING] [Window.setMenuRender]" \
				+ " Unknown gameId %s" % gameId)
			gameId = 0

		print("[INFO] [Window.setMenuRender] Creating menu" \
			+ " activity with gameId=%s" % gameId)
		self.activity = Menu_activity(self, gameId)

	def setGameRender(self, gameId):
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

	def drawImage(self, image, pos):
		"""
		Draw an image on the screen.

		:type image: pygame.surface.Surface
		:param image: The surface to draw on the screen.

		:type pos: list<int>
		:param pos: The (x, y) position of the surface on the screen.
			(0, 0) = the top left corner of the screen.
		"""

		x, y = int(pos[0]), int(pos[1])
		self.root_window.blit(image, (x + 5, y + 5))

	def getOption(self, optionKey):
		"""
		Get an option value.

		:type optionKey: str
		:param optionKey: The option name.

		:rtype: object
		:returns: The option's value.
		"""

		if optionKey in self.options:
			return self.options[optionKey]

	def setOption(self, optionKey, optionValue):
		"""
		Define a new option or modify an existing one.

		:type optionKey: str
		:param optionKey: The name of the option to define.

		:type optionValue: object
		:param optionValue: The value of the option.
		"""
		self.options[optionKey] = optionValue

	def getSize(self):
		"""
		Return the size of the game window.

		:rtype: tuple
		:returns: A (width, height) tuple.
		"""
		if self.root_window:
			w, h = self.root_window.get_size()
			return w - 10, h - 10

	@staticmethod
	def getScreenSize():
		"""
		Return the size of the default screen.
		@staticmethod

		:rtype: tuple
		:returns: A (width, height) tuple.
		"""

		infos = pygame.display.Info()
		return infos.current_w, infos.current_h
