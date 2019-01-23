# -*- coding: utf-8 -*-

"""
Game activities. Manage the views.

Created on 17/01/2019
"""

from game.config import MUSIC_PATH
from game.util import loadImages, loadSounds, Game
from graphism.level_drawer import Level_drawer

__author__ = "Julien Dubois"
__version__ = "2.0.0"

from lemapi.activity import Activity
from lemapi.api import force_view_update, get_listener_manager, stop_app, \
	get_gui, get_audio_player
from lemapi.audio import Mixer
from lemapi.event_manager import Event
from os.path import join
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
		self.exitFct(Game.options.get("last game", 0))



class Menu_activity(Activity):
	def __init__(self, view, playFct, gameId):
		self.playFct = playFct
		self.gameId = gameId
		self.levelDrawer = Level_drawer(get_gui(), gameId, botMode = True)
		self.mixer = Mixer(get_audio_player())

		get_audio_player().add_mixer(self.mixer)
		super().__init__(view)

		self.initEvents()
		self.initScore()
		self.initSounds()

	def initEvents(self):
		event = Event(self.playFct, 0)
		self.view.widgets["play_button"].clickEvents.append(event)
		event = Event(self.playFct, 1)
		self.view.widgets["play_button_2"].clickEvents.append(event)
		event = Event(self.onClickOption)
		self.view.widgets["option_button"].clickEvents.append(event)
		event = Event(stop_app)
		self.view.widgets["quit_button"].clickEvents.append(event)

	def initScore(self):
		scores = Game.options.get("high score", (0, 0))
		self.view.widgets["play_button"].config(text=scores[0])
		if scores[0] >= 10000:
			self.view.widgets["play_button_2"].config(text=scores[1])
		else:
			self.view.widgets["play_button_2"].config(enable=False)

	def initSounds(self):
		ap = get_audio_player()
		msc = ap.get_music(join(MUSIC_PATH, "intro.wav"))
		msc.play()
		msc.set_play_count(-1)
		self.mixer.add_music(msc)

	def onClickOption(self):
		for widget in self.view.widgets.values():
			widget.config(enable=False)
		sv = Game.options.get("sound volume", 1)
		mv = Game.options.get("music volume", 1)
		self.view.createOptionMenu(self.onOptionMenuDestroy, lambda x, y: None, \
			(sv, mv))

	def onOptionMenuDestroy(self):
		self.view.remove_widget("option_menu")
		for widget in self.view.widgets.values():
			widget.config(enable=True)
		self.view.widgets["play_button_2"].config(enable = self.isPyoro2Unlocked())

	def update(self, deltaTime):
		self.levelDrawer.update(deltaTime)
		super().update(deltaTime)

	def isPyoro2Unlocked(self):
		"""
		Check if Pyoro 2 is unlocked. To unlock Pyoro 2, the score must be
			greater than 10000.

		:rtype: bool
		:returns: True if Pyoro 2 is unlocked, otherwise False.
		"""

		highScore = Game.options.get("high score", [0, 0])
		return highScore[0] >= 10000

	def destroy(self):
		get_audio_player().remove_mixer(self.mixer)
		self.mixer.clear()
		super().destroy()


class Level_activity(Activity):
	def __init__(self, view, exitFct, gameId):
		self.exitFct = exitFct
		self.gameId = gameId
		self.levelDrawer = Level_drawer(get_gui(), gameId)
		self.pauseEvent = None
		self.mixer = Mixer(get_audio_player())
		self.musics = {}
		self.last_score = 0

		get_audio_player().add_mixer(self.mixer)
		super().__init__(view)

		self.initEvents()
		self.initScore()
		self.initSounds()

	def initEvents(self):
		lmgr = get_listener_manager()
		# key down
		self.pauseEvent = Event(self.onPauseGame)
		lmgr.add_key_down_event(self.pauseEvent, K_ESCAPE)
		event = Event(self.levelDrawer.level.pyoro.enableMoveRight)
		lmgr.add_key_down_event(event, K_RIGHT)
		event = Event(self.levelDrawer.level.pyoro.enableMoveLeft)
		lmgr.add_key_down_event(event, K_LEFT)
		event = Event(self.levelDrawer.level.pyoro.enableCapacity)
		lmgr.add_key_down_event(event, K_SPACE)

		# key up
		event = Event(self.levelDrawer.level.pyoro.disableMove)
		lmgr.add_key_up_event(event, K_RIGHT)
		event = Event(self.levelDrawer.level.pyoro.disableMove)
		lmgr.add_key_up_event(event, K_LEFT)
		event = Event(self.levelDrawer.level.pyoro.disableCapacity)
		lmgr.add_key_up_event(event, K_SPACE)

	def initScore(self):
		hs = self.getHighScore()
		self.view.widgets["high_score_text"].text = "Meilleur score : %s" % hs

	def initSounds(self):
		music_names = ("drums.wav", "game_over.wav", "music_0.wav", \
			"music_1.wav", "music_2.wav", "organ.wav", "speed_drums.wav")
		ap = get_audio_player()
		for music_name in music_names:
			self.musics[music_name] = ap.get_music(music_name)
			self.musics[music_name].set_play_count(-1)
			self.mixer.add_music(self.musics[music_name])
		self.musics["game_over.wav"].set_play_count(1)
		self.musics["music_0.wav"].play()

	def onClickOption(self):
		for widget in self.view.widgets.values():
			widget.config(enable=False)
		sv = Game.options.get("sound volume", 1)
		mv = Game.options.get("music volume", 1)
		self.view.createOptionMenu(self.onOptionMenuDestroy, lambda x, y: None, \
			(sv, mv))

	def onOptionMenuDestroy(self):
		self.view.remove_widget("option_menu")
		for widget in self.view.widgets.values():
			widget.config(enable=True)
		self.view.widgets["play_button_2"].config(enable = self.isPyoro2Unlocked())

	def onPauseGame(self):
		self.view.createPauseMenu(self.onPauseMenuDestroy, self.exitFct, \
			self.onClickOption)
		self.levelDrawer.level.loopActive = False
		self.mixer.pause()
		self.levelDrawer.level.mixer.pause()

		lmgr = get_listener_manager()
		lmgr.remove_event(self.pauseEvent)
		self.pauseEvent = Event(self.onPauseMenuDestroy)
		lmgr.add_key_down_event(self.pauseEvent, K_ESCAPE)

	def onPauseMenuDestroy(self):
		self.view.remove_widget("pause_menu")
		self.levelDrawer.level.loopActive = True
		self.mixer.play()
		self.levelDrawer.level.mixer.play()

		lmgr = get_listener_manager()
		lmgr.remove_event(self.pauseEvent)
		self.pauseEvent = Event(self.onPauseGame)
		lmgr.add_key_down_event(self.pauseEvent, K_ESCAPE)

	def onGameOver(self):
		self.view.createGameOverMenu(self.onGameOverMenuDestroy, \
			self.levelDrawer.level.score)
		lmgr = get_listener_manager()
		lmgr.remove_event(self.pauseEvent)

	def onGameOverMenuDestroy(self):
		"""
		This method is called when the game over menu is destroyed. It makes the
		game return to the main menu.
		"""

		self.view.remove_widget("game_over_menu")
		self.exitFct(self.gameId)

	def update(self, deltaTime):
		self.levelDrawer.update(deltaTime)
		self.updateScore()
		self.updateSounds(deltaTime)
		super().update(deltaTime)

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

		self.view.widgets["score_text"].text = \
			"Score: %s" % self.levelDrawer.level.score

		if self.levelDrawer.level.score > self.getHighScore():
			self.view.widgets["high_score_text"].text = \
				"High Score: %s" % self.levelDrawer.level.score

	def updateSounds(self, deltaTime):
		s = self.levelDrawer.level.score
		if s >= 5000 and self.last_score < 5000:
			self.musics["drums.wav"].play()
			self.musics["drums.wav"].set_pos(self.musics["music_0.wav"].pos)
		if s >= 10000 and self.last_score < 10000:
			self.musics["organ.wav"].play()
			self.musics["organ.wav"].set_pos(self.musics["music_0.wav"].pos)
		if s >= 20000 and self.last_score < 20000:
			self.musics["drums.wav"].stop()
			self.musics["organ.wav"].stop()
			self.musics["music_0.wav"].stop()
			self.mixer.set_speed(1)
			self.musics["music_1.wav"].play()
		if s >= 30000 and self.last_score < 30000:
			self.musics["music_1.wav"].stop()
			self.mixer.set_speed(1)
			self.musics["music_2.wav"].play()
		if s >= 41000 and self.last_score < 41000:
			self.musics["speed_drums.wav"].play()
			self.musics["speed_drums.wav"].set_pos(self.musics["music_2.wav"].pos)
		self.last_score = s
		self.mixer.set_speed(self.mixer.get_speed() + 0.002 * deltaTime)

	def saveLevelState(self):
		"""
		Save the score and the gameId of the current level.
		"""

		if self.levelDrawer.level.score > self.getHighScore():
			self.setHighScore(self.levelDrawer.level.score)
		Game.options["last game"] = self.levelDrawer.level.gameId

	def update(self, deltaTime):
		"""
		Update all graphical components of this activity.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last call of this method (in
			seconds).
		"""

		self.levelDrawer.update(deltaTime)
		self.updateScore()
		super().update(deltaTime)

	def destroy(self):
		"""
		Destroy the activity and all its components.
		"""

		self.saveLevelState()
		get_audio_player().remove_mixer(self.mixer)
		self.mixer.clear()
		super().destroy()
