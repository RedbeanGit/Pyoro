# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 10/04/2018
	@version: 1
=========================
"""

import os, pygame
from pygame.locals import KEYDOWN, KEYUP, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION, JOYAXISMOTION

from game.config import LEVEL_IMAGE_PATH
from game.level import Level
from game.util import Game

from gui.game_over_menu import Game_over_menu
from gui.image_transformer import Image_transformer
from gui.activity import Activity
from gui.pause_menu import Pause_menu
from gui.text import Text
from gui.level_drawer import Level_drawer

class Level_activity(Activity):
	""" Activity managing the level's components """

	# init some data
	def __init__(self, window, gameId = 0):
		self.window = window
		self.level = Level(self, gameId)
		self.levelDrawer = Level_drawer(self.level, self.window)

		self.lastLevelStyleType = 0
		self.lastLevelScore = 0

		self.joyHatStates = []
		self.joyAxisStates = []

		self.initJoyStates()
		self.level.init()
		Activity.__init__(self, window)

	def initImages(self):
		self.levelDrawer.initImages()
		Activity.initImages(self)

	def initSounds(self):
		self.__initSounds__(("music_0", "music_1", "music_2",
			"drums", "organ", "game_over", "speed_drums"),
			os.path.join("data", "audio", "musics"), "music")
		self.sounds["music_0"].play()

	def initWidgets(self):
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
		bestJoyHats = max(self.window.joysticks, key = lambda x: x.get_numhats(), default = None)
		bestJoyAxis = max(self.window.joysticks, key = lambda x: x.get_numaxes(), default = None)
		if bestJoyHats:
			for i in range(bestJoyHats.get_numhats()):
				self.joyHatStates.append(None)
		if bestJoyAxis:
			for i in range(bestJoyAxis.get_numaxes()):
				self.joyAxisStates.append(None)

	# score
	def getHighScore(self):
		return self.window.getOption("high score")[self.level.gameId]

	def setHighScore(self, score):
		lastOptions = self.window.getOption("high score")
		lastOptions[self.level.gameId] = score
		self.window.setOption("high score", lastOptions)

	def updateScore(self):
		self.widgets["score_text"].text = "Score: %s" % self.level.score
		if self.level.score > self.getHighScore():
			self.widgets["high_score_text"].text = "High Score: %s" % self.level.score


	# sounds
	def updateSounds(self, deltaTime):
		styleType = self.level.getStyleTypeWithScore()
		if styleType == 0:
			if self.lastLevelScore != self.level.score:

				if self.lastLevelScore < 5000 and self.level.score >= 5000:
					print("[INFO] [Level_activity.updateSounds] Drums added to the music")
					self.sounds["drums"].play()
					self.sounds["drums"].setPos(self.sounds["music_0"].pos)

				elif self.lastLevelScore < 10000 and self.level.score >= 10000:
					print("[INFO] [Level_activity.updateSounds] Organ added to the music")
					self.sounds["organ"].play()
					self.sounds["organ"].setPos(self.sounds["music_0"].pos)

		elif styleType == 1:
			if self.lastLevelStyleType != styleType:
				print("[INFO] [Level_activity.updateSounds] Music 2 started")
				Game.audioPlayer.setSpeed(1)
				Game.audioPlayer.stopAudio()
				self.sounds["music_1"].play()

		elif styleType == 2:
			if self.lastLevelStyleType != styleType:
				print("[INFO] [Level_activity.updateSounds] Music 3 started")
				Game.audioPlayer.setSpeed(1)
				Game.audioPlayer.stopAudio()
				self.sounds["music_2"].play()

			if self.lastLevelScore < 41000 and self.level.score >= 41000:
				print("[INFO] [Level_activity.updateSounds] Speed drums added to the music")
				self.sounds["speed_drums"].play()
				self.sounds["speed_drums"].setPos(self.sounds["music_2"].pos)

		self.lastLevelStyleType = styleType
		self.lastLevelScore = self.level.score
		if not self.level.pyoro.dead:
			Game.audioPlayer.setSpeed(Game.audioPlayer.getSpeed() + 0.002 * deltaTime)

	def saveLevelState(self):
		if self.level.score > self.getHighScore():
			self.setHighScore(self.level.score)
		self.window.setOption("last game", self.level.gameId)

	def pauseGame(self):
		if "pause_menu" in self.widgets:
			self.widgets["pause_menu"].destroy()
		else:
			#Game.audioPlayer.pauseAudio()
			size = self.layout.getWidgetSize("pause_menu")
			pos = self.layout.getWidgetPos("pause_menu")
			anchor = self.layout.getWidgetAnchor("pause_menu")

			self.addWidget("pause_menu", Pause_menu, pos, \
				self.onPauseMenuDestroy, self.window.setMenuRender, \
				size = size, anchor = anchor)

			self.level.loopActive = False

	def onPauseMenuDestroy(self):
		self.removeWidget("pause_menu")
		self.level.loopActive = True
		#Game.audioPlayer.unpauseAudio()

	def gameOver(self):
		Game.audioPlayer.stopAudio()
		Game.audioPlayer.setSpeed(1)
		self.sounds["game_over"].play(1)

		size = self.layout.getWidgetSize("game_over_menu")
		pos = self.layout.getWidgetPos("game_over_menu")
		anchor = self.layout.getWidgetAnchor("game_over_menu")
		self.addWidget("game_over_menu", Game_over_menu, pos, self.level.score, \
			self.onGameOverMenuDestroy, size = size, anchor = anchor)

	def onGameOverMenuDestroy(self):
		self.removeWidget("game_over_menu")
		self.window.setMenuRender()



	def updateEvent(self, event):
		if self.level.loopActive:
			keyboard = self.window.getOption("keyboard")
			joystick = self.window.getOption("joystick")

			enableKeys = {
				"left": self.level.pyoro.enableMoveLeft,
				"right": self.level.pyoro.enableMoveRight,
				"action": self.level.pyoro.enableCapacity,
				"pause": self.pauseGame
			}
			disableKeys = {
				"left": self.level.pyoro.disableMove,
				"right": self.level.pyoro.disableMove,
				"action": self.level.pyoro.disableCapacity,
				"pause": lambda:None
			}

			if event.type == KEYDOWN:
				for actionName, action in enableKeys.items():
					if event.key == keyboard[actionName]:
						action()

			elif event.type == KEYUP:
				for actionName, action in disableKeys.items():
					if event.key == keyboard[actionName]:
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
		self.level.update(deltaTime)
		self.levelDrawer.update(deltaTime)

		if self.level.loopActive:
			self.updateScore()
			self.updateSounds(deltaTime)
		Activity.update(self, deltaTime)

	def destroy(self):
		self.saveLevelState()
		Activity.destroy(self)
