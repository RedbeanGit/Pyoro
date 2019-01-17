# -*- coding: utf-8 -*-

"""
Game activities. Manage the views.

Created on 17/01/2019
"""

from game.util import loadImages, Game

__author__ = "Julien Dubois"
__version__ = "2.0.0"

from lemapi.activity import Activity
from lemapi.api import force_view_update


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
        Game.audioPlayer.loadAudio()
		Game.audioPlayer.soundVolume = Game.options.get("sound volume", 1)
		Game.audioPlayer.musicVolume = Game.options.get("music volume", 1)
		Game.audioPlayer.start()
        self.setInfo("Terminé !")
        self.exitFct(Game.options.get("last game", 0))



class Menu_activity(Activity):
    def __init__(self, view, playFct, gameId):
        self.playFct = playFct
        self.levelDrawer = Level_drawer(self, gameId, botMode = True)
        super().__init__(view)

    def onClickOption(self):
        self.view.createOptionMenu(self.onOptionMenuDestroy)

    def onOptionMenuDestroy(self):
        self.view.widgets["play_button_2"].config(enable = self.isPyoro2Unlocked())
		self.removeWidget("option_menu")

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


class Level_activity(Activity):
    def __init__(self, view, exitFct, gameId):
        self.exitFct = exitFct
        self.gameId = gameId
        self.levelDrawer = Level_drawer(self, gameId)
        super().__init__(view)

    def onClickOption(self):
        self.view.createOptionMenu(self.onOptionMenuDestroy)

    def onOptionMenuDestroy(self):
        self.view.widgets["play_button_2"].config(enable = self.isPyoro2Unlocked())
		self.view.remove_widget("option_menu")

    def update(self, deltaTime):
        self.levelDrawer.update(deltaTime)
        self.updateScore()
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

    def saveLevelState(self):
		"""
		Save the score and the gameId of the current level.
		"""

		if self.levelDrawer.level.score > self.getHighScore():
			self.setHighScore(self.levelDrawer.level.score)
		Game.options["last game"] = self.levelDrawer.level.gameId

    def onPauseGame(self):
        self.view.createPauseMenu(self.onPauseMenuDestroy)
        self.levelDrawer.level.loopActive = False

    def onPauseMenuDestroy(self):
        self.levelDrawer.level.loopActive = True
        self.view.remove_widget("pause_menu")

    def onGameOver(self):
        self.view.createGameOverMenu(self.onGameOverMenuDestroy, \
            self.levelDrawer.level.score)

    def onGameOverMenuDestroy(self):
		"""
		This method is called when the game over menu is destroyed. It makes the
		game return to the main menu.
		"""

		self.view.remove_widget("game_over_menu")
		self.exitFct(self.gameId)

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
		super().destroy(self)
