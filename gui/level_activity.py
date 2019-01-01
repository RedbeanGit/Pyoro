# -*- coding: utf-8 -*-

"""
Provide an activity to manage the real game view.

Created on 10/04/2018
"""

from game.config import LEVEL_IMAGE_PATH
from game.level import Level
from game.util import Game

from gui.activity import Activity
from gui.game_over_menu import Game_over_menu
from gui.level_drawer import Level_drawer
from gui.pause_menu import Pause_menu
from gui.text import Text

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import os
import pygame

from pygame.locals import KEYDOWN, KEYUP, JOYBUTTONDOWN, JOYBUTTONUP, \
	JOYHATMOTION, JOYAXISMOTION


class Level_activity(Activity):
	"""
	Activity managing in-game graphical components.
	"""

	def __init__(self, window, gameId = 0):
		"""
		Initialize a new Level_activity object.

		:type window: gui.window.Window
		:param window: The parent game window.

		:type gameId: int
		:param gameId: (Optional) The id of the game to load. It can be 0 or 1.
			0 = Pyoro, 1 = Pyoro 2. Default is 0.
		"""

		self.window = window
		self.levelDrawer = Level_drawer(self, gameId)

		self.lastLevelStyleType = 0
		self.lastLevelScore = 0

		self.joyHatStates = []
		self.joyAxisStates = []

		Activity.__init__(self, window)
		self.initJoyStates()

	def initSounds(self):
		"""
		Load sounds and musics which will be used later by this activity.
		"""

		self.__initSounds__(("music_0", "music_1", "music_2",
			"drums", "organ", "game_over", "speed_drums"),
			os.path.join("data", "audio", "musics"), "music")
		Game.audioPlayer.setSpeed(1)
		self.sounds["music_0"].play(-1)

	def initWidgets(self):
		"""
		Create widgets which will be used later by this activity ("score" and "high
		score" text).
		"""

		spos = self.layout.getWidgetPos("score_text")
		ssize = self.layout.getFontSize("score_text")

		hpos = self.layout.getWidgetPos("high_score_text")
		hsize = self.layout.getFontSize("high_score_text")

		self.addWidget("score_text", Text, spos, "Score: 0", \
			fontSize = ssize, anchor = (0, -1))
		self.addWidget("high_score_text", Text, hpos, \
			"Meilleur Score: %s" % self.getHighScore(), \
			fontSize = hsize, anchor = (0, -1))

	def initJoyStates(self):
		"""
		Initialize joystick hat and axis values.
		"""

		bestJoyHats = max(self.window.joysticks, key = lambda x: x.get_numhats(),
			default = None)
		bestJoyAxis = max(self.window.joysticks, key = lambda x: x.get_numaxes(),
			default = None)
		if bestJoyHats:
			for i in range(bestJoyHats.get_numhats()):
				self.joyHatStates.append(None)
		if bestJoyAxis:
			for i in range(bestJoyAxis.get_numaxes()):
				self.joyAxisStates.append(None)

	# score
	def getHighScore(self):
		"""
		Return the highest score from options.

		:rtype: int
		:returns: The highest score for the current gameId.
		"""

		return Game.options.get("high score", [0, 0])[self.levelDrawer.level.gameId]

	def setHighScore(self, score):
		"""
		Define a new high score for the current gameId.
		"""

		if "high score" not in Game.options:
			Game.options["high score"] = [0, 0]
		Game.options["high score"][self.levelDrawer.level.gameId] = score

	def updateScore(self):
		"""
		Update the score text widget with the current score.
		"""

		self.widgets["score_text"].text = "Score: %s" % self.levelDrawer.level.score
		if self.levelDrawer.level.score > self.getHighScore():
			self.widgets["high_score_text"].text = \
				"High Score: %s" % self.levelDrawer.level.score


	def updateSounds(self, deltaTime):
		"""
		Start or stop musics according to the current score.
		"""

		styleType = self.levelDrawer.level.getStyleTypeWithScore()

		# Normal style
		if styleType == 0:
			if self.lastLevelScore != self.levelDrawer.level.score:

				if self.lastLevelScore < 5000 and self.levelDrawer.level.score >= 5000:
					print("[INFO] [Level_activity.updateSounds] Drums added to the music")
					self.sounds["drums"].play(-1)
					self.sounds["drums"].setPos(self.sounds["music_0"].pos)

				elif self.lastLevelScore < 10000 and self.levelDrawer.level.score >= 10000:
					print("[INFO] [Level_activity.updateSounds] Organ added to the music")
					self.sounds["organ"].play(-1)
					self.sounds["organ"].setPos(self.sounds["music_0"].pos)

		# Black and white style
		elif styleType == 1:
			if self.lastLevelStyleType != styleType:
				print("[INFO] [Level_activity.updateSounds] Music 2 started")
				Game.audioPlayer.setSpeed(1)
				Game.audioPlayer.stopAudio()
				self.sounds["music_1"].play(-1)

		# Flashy style
		elif styleType == 2:
			if self.lastLevelStyleType != styleType:
				print("[INFO] [Level_activity.updateSounds] Music 3 started")
				Game.audioPlayer.setSpeed(1)
				Game.audioPlayer.stopAudio()
				self.sounds["music_2"].play(-1)

			if self.lastLevelScore < 41000 and self.levelDrawer.level.score >= 41000:
				print("[INFO] [Level_activity.updateSounds] Speed drums added to the music")
				self.sounds["speed_drums"].play(-1)
				self.sounds["speed_drums"].setPos(self.sounds["music_2"].pos)

		self.lastLevelStyleType = styleType
		self.lastLevelScore = self.levelDrawer.level.score
		if not self.levelDrawer.level.pyoro.dead:
			Game.audioPlayer.setSpeed(Game.audioPlayer.getSpeed() + 0.002 * deltaTime)

	def saveLevelState(self):
		"""
		Save the score and the gameId of the current level.
		"""

		if self.levelDrawer.level.score > self.getHighScore():
			self.setHighScore(self.levelDrawer.level.score)
		Game.options["last game"] = self.levelDrawer.level.gameId

	def pauseGame(self):
		"""
		Stop updating the level.
		"""

		if "pause_menu" in self.widgets:
			self.onPauseMenuDestroy()
		else:
			if "game_over_menu" not in self.widgets:
				#Game.audioPlayer.pauseAudio()
				size = self.layout.getWidgetSize("pause_menu")
				pos = self.layout.getWidgetPos("pause_menu")
				anchor = self.layout.getWidgetAnchor("pause_menu")
				fsize = self.layout.getFontSize("pause_menu")

				self.addWidget("pause_menu", Pause_menu, pos, \
					self.onPauseMenuDestroy, self.window.setMenuRender, \
					size = size, anchor = anchor, fontSize = fsize)
				self.levelDrawer.level.loopActive = False

	def onPauseMenuDestroy(self):
		"""
		This method is called when the pause menu is destroyed. It re-enable the
		level to be updated.
		"""

		self.removeWidget("pause_menu")
		self.levelDrawer.level.loopActive = True
		#Game.audioPlayer.unpauseAudio()

	def gameOver(self):
		"""
		Stop sounds and create a "game over" menu dialog.
		"""

		Game.audioPlayer.stopAudio()
		Game.audioPlayer.setSpeed(1)
		self.sounds["game_over"].play()

		size = self.layout.getWidgetSize("game_over_menu")
		pos = self.layout.getWidgetPos("game_over_menu")
		anchor = self.layout.getWidgetAnchor("game_over_menu")
		fsize = self.layout.getFontSize("game_over_menu")

		self.addWidget("game_over_menu", Game_over_menu, pos, \
			self.levelDrawer.level.score, self.onGameOverMenuDestroy, \
			size = size, anchor = anchor, fontSize = fsize)

	def onGameOverMenuDestroy(self):
		"""
		This method is called when the game over menu is destroyed. It makes the
		game return to the main menu.
		"""

		self.removeWidget("game_over_menu")
		self.window.setMenuRender()

	def updateEvent(self, event):
		"""
		Update the level with
		"""

		if self.levelDrawer.level.loopActive:
			keyboard = Game.options.get("keyboard", {})
			joystick = Game.options.get("joystick", {})
			pyoro = self.levelDrawer.level.pyoro

			enableKeys = {
				"left": pyoro.enableMoveLeft,
				"right": pyoro.enableMoveRight,
				"action": pyoro.enableCapacity,
				"pause": self.pauseGame
			}
			disableKeys = {
				"left": pyoro.disableMove,
				"right": pyoro.disableMove,
				"action": pyoro.disableCapacity,
				"pause": lambda:None
			}

			if event.type == KEYDOWN:
				for actionName, action in enableKeys.items():
					if event.key == keyboard.get(actionName, None):
						action()

			elif event.type == KEYUP:
				for actionName, action in disableKeys.items():
					if event.key == keyboard.get(actionName, None):
						action()

			elif event.type == JOYBUTTONDOWN:
				for actionName, inputInfos in joystick.items():
					if inputInfos["inputType"] == JOYBUTTONDOWN:
						if inputInfos["buttonId"] == event.button:
							enableKeys[actionName]()

			elif event.type == JOYBUTTONUP:
				for actionName, inputInfos in joystick.items():
					if inputInfos["inputType"] == JOYBUTTONDOWN:
						if inputInfos["buttonId"] == event.button:
							disableKeys[actionName]()

			elif event.type == JOYHATMOTION:
				enabled = event.value
				disabled = self.joyHatStates[event.hat]
				self.joyHatStates[event.hat] = enabled

				for actionName, inputInfos in joystick.items():
					if inputInfos["inputType"] == JOYHATMOTION:
						if inputInfos["hatId"] == event.hat:
							if inputInfos["value"] == enabled:
								enableKeys[actionName]()
							elif inputInfos["value"] == disabled:
								disableKeys[actionName]()

			elif event.type == JOYAXISMOTION:
				enabled = event.value
				disabled = self.joyAxisStates[event.axis]
				self.joyAxisStates[event.axis] = enabled

				for actionName, inputInfos in joystick.items():
					if inputInfos["inputType"] == JOYAXISMOTION:
						if inputInfos["axisId"] == event.axis:
							if inputInfos["value"] / enabled > 0 and abs(event.value) > 0.2:
								enableKeys[actionName]()
							elif disabled:
								if inputInfos["value"] / disabled > 0 or abs(event.value) <= 0.2:
									disableKeys[actionName]()

		Activity.updateEvent(self, event)

	def update(self, deltaTime):
		"""
		Update all graphical components of this activity.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last call of this method (in
			seconds).
		"""

		self.levelDrawer.update(deltaTime)
		if self.levelDrawer.level.loopActive:
			self.updateScore()
			self.updateSounds(deltaTime)
		Activity.update(self, deltaTime)

	def destroy(self):
		"""
		Destroy the activity and all its components.
		"""

		self.saveLevelState()
		Activity.destroy(self)
