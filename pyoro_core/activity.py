# -*- coding: utf-8 -*-

"""
Game activities. Manage the views.

Created on 17/01/2019
"""


from pyoro_core.constants import MUSIC_PATH, Game
from pyoro_core.util import loadImages, loadSounds
from pyoro_core.level_drawer import Level_drawer

__author__ = "Julien Dubois"
__version__ = "2.0.0"

import os

from lemapi.activity import Activity
from lemapi.api import force_view_update, stop_app, get_gui, get_audio_player
from lemapi.audio import Mixer
from lemapi.event_manager import Event

from pygame.locals import K_ESCAPE, K_RIGHT, K_LEFT, K_SPACE


class Splash_activity(Activity):
	def __init__(self, view, exitFct):
		self.exitFct = exitFct
		super().__init__(view)

	def setInfo(self, msg):
		self.view.widgets["info_text"].text = msg
		force_view_update()

	def boot(self):
		self.setInfo("Chargement des images...")
		loadImages()
		self.setInfo("Chargement des sons...")
		loadSounds()
		self.setInfo("Terminé !")
		self.exitFct(Game.OPTIONS.get("last game", 0))


class Menu_activity(Activity):
	def __init__(self, view, playFct, gameId):
		self.playFct = playFct
		self.gameId = gameId
		self.levelDrawer = Level_drawer(get_gui(), gameId, botMode=True)
		self.mixer = None

		super().__init__(view)

		self.initEvents()
		self.initScore()
		self.initMixer()

		self.start_music()

	def initEvents(self):
		event = Event(self.playFct, 0)
		self.view.widgets["play_button"].endClickEvents.append(event)
		event = Event(self.playFct, 1)
		self.view.widgets["play_button_2"].endClickEvents.append(event)
		event = Event(self.onClickOption)
		self.view.widgets["option_button"].endClickEvents.append(event)
		event = Event(stop_app)
		self.view.widgets["quit_button"].endClickEvents.append(event)
		self.listener_manager.km.add_key_down_event(event, K_ESCAPE)
		self.listener_manager.cm.add_button_pressed_event(event, "button_b")

	def initScore(self):
		scores = Game.OPTIONS.get("high score", (0, 0))
		self.view.widgets["play_button"].config(text=scores[0])
		if scores[0] >= 10000:
			self.view.widgets["play_button_2"].config(text=scores[1])
		else:
			self.view.widgets["play_button_2"].config(enable=False)

	def initMixer(self):
		ap = get_audio_player()
		self.mixer = Mixer(ap)
		ap.add_mixer(self.mixer)

		self.setSoundVolume(Game.OPTIONS.get("sound volume", 1), \
			Game.OPTIONS.get("music volume", 1))

	def start_music(self):
		ap = get_audio_player()
		msc = ap.get_music(os.path.join(MUSIC_PATH, "intro.wav"))
		msc.play()
		msc.set_play_count(-1)
		self.mixer.add_music(msc)

	def onClickOption(self):
		for widget in self.view.widgets.values():
			widget.config(enable=False)

		sv = Game.OPTIONS.get("sound volume", 1)
		mv = Game.OPTIONS.get("music volume", 1)

		self.view.createOptionMenu(self.onOptionMenuDestroy, self.setSoundVolume, (sv, mv))

	def onOptionMenuDestroy(self):
		self.view.remove_widget("option_menu")

		for widget in self.view.widgets.values():
			widget.config(enable=True)
		
		self.view.widgets["play_button_2"].config(enable=self.isPyoro2Unlocked())

	def setSoundVolume(self, sound, music):
		self.mixer.set_volume(music)

		Game.OPTIONS["sound volume"] = sound
		Game.OPTIONS["music volume"] = music

	def update(self, deltaTime):
		self.levelDrawer.update(deltaTime)

		scores = Game.OPTIONS.get("high score", [0, 0])
		self.view.widgets["play_button"].config(text=scores[0])
		self.view.widgets["play_button_2"].config(text=scores[1])

		super().update(deltaTime)

	def isPyoro2Unlocked(self):
		highScore = Game.OPTIONS.get("high score", [0, 0])
		return highScore[0] >= 10000

	def stopMixer(self):
		self.mixer.clear()
		get_audio_player().remove_mixer(self.mixer)

	def sleep(self):
		self.stopMixer()
		super().sleep()

	def wakeup(self):
		self.initMixer()
		self.start_music()
		super().wakeup()

	def destroy(self):
		self.stopMixer()
		super().destroy()


class Level_activity(Activity):
	def __init__(self, view, exitFct, gameId):
		self.exitFct = exitFct
		self.gameId = gameId
		self.levelDrawer = Level_drawer(get_gui(), gameId)
		self.pauseEvents = []
		self.mixer = None
		self.musics = {}

		self.lastScore = 0
		self.gameOverListener = True

		super().__init__(view)

		self.initEvents()
		self.initScore()
		self.initMixer()

	def initEvents(self):
		lmgr = self.listener_manager
		# key down
		event = Event(self.onPauseGame)
		self.pauseEvents.append(event)
		lmgr.km.add_key_down_event(event, K_ESCAPE, copy=False)
		event = Event(self.onPauseGame)
		self.pauseEvents.append(event)
		lmgr.cm.add_button_pressed_event(event, "button_b", copy=False)

		event = Event(self.levelDrawer.level.pyoro.enableMoveRight)
		lmgr.km.add_key_down_event(event, K_RIGHT)
		lmgr.cm.add_joy_right_event(event)

		event = Event(self.levelDrawer.level.pyoro.enableMoveLeft)
		lmgr.km.add_key_down_event(event, K_LEFT)
		lmgr.cm.add_joy_left_event(event)

		event = Event(self.levelDrawer.level.pyoro.enableCapacity)
		lmgr.km.add_key_down_event(event, K_SPACE)
		lmgr.cm.add_button_pressed_event(event, "button_a")

		# key up
		event = Event(self.levelDrawer.level.pyoro.disableMove)
		lmgr.km.add_key_up_event(event, K_RIGHT)
		lmgr.cm.add_joy_dead_event(event)

		event = Event(self.levelDrawer.level.pyoro.disableMove)
		lmgr.km.add_key_up_event(event, K_LEFT)
		lmgr.cm.add_joy_dead_event(event)

		event = Event(self.levelDrawer.level.pyoro.disableCapacity)
		lmgr.km.add_key_up_event(event, K_SPACE)
		lmgr.cm.add_button_released_event(event, "button_a")

	def initScore(self):
		hs = self.getHighScore()
		self.lastScore = 0
		self.view.widgets["high_score_text"].text = "Meilleur score : %s" % hs

	def initMixer(self):
		music_names = ("drums.wav", "game_over.wav", "music_0.wav", \
			"music_1.wav", "music_2.wav", "organ.wav", "speed_drums.wav")
		ap = get_audio_player()
		ap.set_speed(1)
		self.mixer = Mixer(ap)
		ap.add_mixer(self.mixer)

		self.setSoundVolume(Game.OPTIONS.get("sound volume", 1), \
			Game.OPTIONS.get("music volume", 1))

		for music_name in music_names:
			self.musics[music_name] = ap.get_music(os.path.join(MUSIC_PATH, music_name))
			self.musics[music_name].set_play_count(-1)
			self.mixer.add_music(self.musics[music_name])

		self.musics["game_over.wav"].set_play_count(1)
		self.musics["music_0.wav"].play()

	def onClickOption(self):
		for widget in self.view.widgets.values():
			widget.config(enable=False)
		sv = Game.OPTIONS.get("sound volume", 1)
		mv = Game.OPTIONS.get("music volume", 1)

		for event in self.pauseEvents:
			event.enable = False

		self.view.createOptionMenu(self.onOptionMenuDestroy, self.setSoundVolume, \
			(sv, mv))

	def setSoundVolume(self, sound, music):
		self.mixer.set_volume(music)
		self.levelDrawer.level.mixer.set_volume(sound)

		Game.OPTIONS["sound volume"] = sound
		Game.OPTIONS["music volume"] = music

	def onOptionMenuDestroy(self):
		self.view.remove_widget("option_menu")
		for widget in self.view.widgets.values():
			widget.config(enable=True)

		for event in self.pauseEvents:
			event.enable = True

	def onPauseGame(self):
		self.view.createPauseMenu(self.onPauseMenuDestroy, self.exitFct, \
			self.onClickOption)
		self.levelDrawer.level.loopActive = False
		self.mixer.pause()
		self.levelDrawer.level.mixer.pause()

		for event in self.pauseEvents:
			event.fct = self.onPauseMenuDestroy

	def onPauseMenuDestroy(self):
		self.view.remove_widget("pause_menu")
		self.levelDrawer.level.loopActive = True
		self.mixer.play()
		self.levelDrawer.level.mixer.play()

		for event in self.pauseEvents:
			event.fct = self.onPauseGame

	def onGameOver(self):
		get_audio_player().set_speed(1)
		self.mixer.stop_audio()
		self.musics["game_over.wav"].play()

		self.view.createGameOverMenu(self.onGameOverMenuDestroy, \
			self.levelDrawer.level.score)

		for event in self.pauseEvents:
			event.enable = False

	def onGameOverMenuDestroy(self):
		self.view.remove_widget("game_over_menu")
		self.exitFct()

	def update(self, deltaTime):
		self.levelDrawer.update(deltaTime)
		self.updateScore()
		self.updateSounds(deltaTime)
		super().update(deltaTime)

	def getHighScore(self):
		return Game.OPTIONS.get("high score", [0, 0])[self.levelDrawer.level.gameId]

	def setHighScore(self, score):
		if "high score" not in Game.OPTIONS:
			Game.OPTIONS["high score"] = [0, 0]
		Game.OPTIONS["high score"][self.levelDrawer.level.gameId] = score

	def updateScore(self):
		self.view.widgets["score_text"].text = \
			"Score: %s" % self.levelDrawer.level.score

		if self.levelDrawer.level.score > self.getHighScore():
			self.view.widgets["high_score_text"].text = \
				"High Score: %s" % self.levelDrawer.level.score

	def updateSounds(self, deltaTime):
		s = self.levelDrawer.level.score
		ap = get_audio_player()

		if s >= 5000 and self.lastScore < 5000:
			print("[INFO] [Level_activity.updateSounds] Drums added")
			self.musics["drums.wav"].play()
			self.musics["drums.wav"].set_pos(self.musics["music_0.wav"].pos)
		if s >= 10000 and self.lastScore < 10000:
			print("[INFO] [Level_activity.updateSounds] Organ added")
			self.musics["organ.wav"].play()
			self.musics["organ.wav"].set_pos(self.musics["music_0.wav"].pos)
		if s >= 20000 and self.lastScore < 20000:
			print("[INFO] [Level_activity.updateSounds] Music 2 started")
			self.musics["drums.wav"].stop()
			self.musics["organ.wav"].stop()
			self.musics["music_0.wav"].stop()
			ap.set_speed(1)
			self.musics["music_1.wav"].play()
		if s >= 30000 and self.lastScore < 30000:
			print("[INFO] [Level_activity.updateSounds] Music 3 started")
			self.musics["music_1.wav"].stop()
			ap.set_speed(1)
			self.musics["music_2.wav"].play()
		if s >= 41000 and self.lastScore < 41000:
			print("[INFO] [Level_activity.updateSounds] Fast drums added")
			self.musics["speed_drums.wav"].play()
			self.musics["speed_drums.wav"].set_pos(self.musics["music_2.wav"].pos)

		self.lastScore = s
		ap.set_speed(ap.speed + 0.002*deltaTime)

	def saveLevelState(self):
		if self.levelDrawer.level.score > self.getHighScore():
			self.setHighScore(self.levelDrawer.level.score)
		Game.OPTIONS["last game"] = self.levelDrawer.level.gameId

	def update(self, deltaTime):
		self.levelDrawer.update(deltaTime)

		if self.levelDrawer.level.loopActive:
			self.updateScore()
			self.updateSounds(deltaTime)

		if self.gameOverListener:
			if self.levelDrawer.level.pyoro.dead:
				self.gameOverListener = False
				self.onGameOver()

		super().update(deltaTime)

	def stopMixer(self):
		self.mixer.clear()
		get_audio_player().remove_mixer(self.mixer)

	def sleep(self):
		self.stopMixer()
		super().sleep()

	def wakeup(self):
		self.initMixer()
		super().wakeup()

	def destroy(self):
		self.levelDrawer.level.endLevel()
		self.saveLevelState()
		self.stopMixer()
		super().destroy()
