# -*- coding: utf-8 -*-

"""
Provide a class to manage a game level (entities, flow of time,...)

Created on 18/03/2018
"""

from entities.angel import Angel
from entities.bean import Bean
from entities.leaf import Leaf
from entities.leaf_piece import Leaf_piece
from entities.pink_bean import Pink_bean
from entities.pyobot import Pyobot
from entities.pyobot_2 import Pyobot_2
from entities.pyoro import Pyoro
from entities.pyoro_2 import Pyoro_2
from entities.score_text import Score_text
from entities.smoke import Smoke
from entities.super_bean import Super_bean

from game.actionDelay import ActionDelay
from game.case import Case
from game.config import BEAN_FREQUENCY, SPEED_ACCELERATION, \
	BACKGROUND_ANIMATED_DURATION
from game.util import Game

__author__ = "Julien Dubois"
__version__ = "1.1"

import os
import random


class Level:
	"""
	Central class that manages the entities, terrain and more.
	"""

	def __init__(self, levelDrawer, gameId, size, botMode = False):
		"""
		Initialize a new Level object.

		:type levelDrawer: gui.level_drawer.Level_drawer
		:param activity: The graphical representation of this level.

		:type gameId: int
		:param gameId: It can be 0 for Pyoro, or 1 for Pyoro 2.

		:type size: tuple
		:param size: The size of the level (in blocks) in a (width, height)
			tuple where width and height are floating point values.

		:type botMode: bool
		:param botMode: Optional. If True, Pyoro will be a bot.
			Default is False.
		"""

		self.levelDrawer = levelDrawer
		self.gameId = gameId
		self.size = size
		self.botMode = botMode

		self.loopActive = True
		self.pyoro = None

		self.score = 0
		self.speed = 1
		self.animatedBackgroundId = 13

		self.cases = []
		self.entities = []
		self.actionDelays = {}

		self.initCases(self.size[0])
		self.initPyoro()
		self.spawnBean()

	def initCases(self, nbCases):
		"""
		Create the terrain with new blocks.

		:type nbCases: int
		:param nbCases: The number of blocks which will compose the floor.
		"""

		self.cases.clear()
		for i in range(nbCases):
			self.cases.append(Case(i))

	def initPyoro(self):
		"""
		Create a new bird according to the current gameId
		and botMode.
		"""

		if self.botMode and self.gameId:
			self.pyoro = Pyobot_2(self)
		elif self.botMode:
			self.pyoro = Pyobot(self)
		elif self.gameId:
			self.pyoro = Pyoro_2(self)
		else:
			self.pyoro = Pyoro(self)

	def reset(self):
		"""
		Restart the level:
			- score = 0
			- speed = 1
			- entities are killed
			- action delayed are stopped
			- terrain is recreated
		"""

		self.score = 0
		self.speed = 1
		for entity in self.entities:
			entity.remove()
		self.entities.clear()
		self.actionDelays.clear()
		self.initCases(self.size[0])
		self.spawnBean()

	def update(self, deltaTime):
		"""
		Update the level, entities and actionDelays.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last update.
		"""

		if self.loopActive:
			self.speed += deltaTime * SPEED_ACCELERATION
			self.pyoro.update(deltaTime * self.speed)
			for entity in self.entities:
				entity.update(deltaTime * self.speed)
			for actionDelay in dict(self.actionDelays).values():
				actionDelay.update(deltaTime * self.speed)

	def updateAnimatedBackground(self):
		"""
		If the current background is animated, update it.
		"""

		if self.animatedBackgroundId < 20:
			self.animatedBackgroundId = self.animatedBackgroundId + 1
		else:
			self.animatedBackgroundId = 13

	def spawnBean(self):
		"""
		Randomly spawn a new bean. Bean type is also random.
		"""

		beanTypeId = random.randint(0, 5)
		pos = (random.randint(0, self.size[0] - 1) + 0.75, 0)
		speed = random.uniform(0.5, 1.5) * (self.speed ** 0.6)

		if beanTypeId < 4:
			bean = Bean(self, pos, speed)
		elif self.score < 5000 or beanTypeId == 4:
			bean = Pink_bean(self, pos, speed)
		else:
			bean = Super_bean(self, pos, speed)

		self.entities.append(bean)
		self.setActionDelay((self, "spawnBean"),
				BEAN_FREQUENCY \
				* random.uniform(0.5, 1.5) \
				/ (self.speed ** 1.5),
				self.spawnBean
			)

	def spawnAngel(self, case):
		"""
		Spawn a new angel only if case can be repaired.

		:type case: game.case.Case
		:param case: The block that will be repaired by the new angel.
		"""

		if not case.exists and not case.isRepairing:
			self.entities.append(Angel(self, case))

	def spawnScore(self, score, pos):
		"""
		Spawn a flashing text and increase the score.

		:type score: int
		:param score: The value to add to the current score.
			It can be 10, 50, 100, 300 or 1000.

		:type pos: Iterable<float>
		:param pos: The position of the flashing text.
		"""

		allowed = (10, 50, 100, 300, 1000)
		if score in allowed:
			self.score += score
			self.entities.append(Score_text(self, pos, score))
		else:
			print("[WARNING] [Level.addScore] %s is an invalid " % score \
				+ "value ! Allowed are %s" % allowed)

	def spawnSmoke(self, pos):
		"""
		Spawn smoke.

		:type pos: Iterable<float>
		:param pos: The position of the smoke.
		"""
		self.entities.append(Smoke(self, pos))

	def spawnLeaf(self, pos, leafType):
		"""
		Spawn leafs with random speed.

		:type pos: Iterable<float>
		:param pos: The position of the leaf.

		:type leafType: str
		:param leafType: The type of the leaf. It can be
			"", "pink" or "super".
		"""

		speed = random.uniform(0.5, 1.5)
		self.entities.append(Leaf(self, pos, speed, leafType))

	def spawnLeafPiece(self, pos, speed, leafPieceType, vel):
		"""
		Spawn cut leaf.

		:type pos: Iterable<float>
		:param pos: The default position of the leaf.

		:type speed: float
		:param speed: The speed of the leaf.

		:type leafPieceType: str
		:param leafPieceType: The type of the leaf. It can be
			"", "pink" or "super".

		:type vel: float
		:param vel: The default horizontal velocity.
		"""
		self.entities.append(Leaf_piece(self, pos, speed, leafPieceType, vel))

	def repairCase(self, case = None):
		"""
		Repair a block by spawning an angel.

		:type case: game.case.Case
		:param case: Optional. The block to repair. The leftmost destroyed
			block is chosen if undefined.
		"""

		voidCases = self.getVoidCases()
		if voidCases:
			case = case if case in voidCases else random.choice(voidCases)
			self.spawnAngel(case)

	def createActionDelay(self, actionName, waitTime, fct, *fctArgs, **fctKwargs):
		"""
		Create a new actionDelay. See game.actionDelay.ActionDelay.
		If an actionDelay already exists with the same name, do nothing.

		:type actionName: object
		:param actionName: The name given to the new actionDelay.

		:type waitTime: float
		:param waitTime: The time to wait before calling fct.

		:type fct: function or method
		:param fct: The function or method to delay.

		:type *fctArgs: object
		:param *fctArgs: The arguments to pass to fct.

		:type **fctKwargs: object
		:param **fctKwargs: The optional arguments to pass to the fct.
		"""

		if actionName not in self.actionDelays:
			self.actionDelays[actionName] = ActionDelay(
				waitTime, fct, *fctArgs, **fctKwargs)

	def setActionDelay(self, actionName, waitTime, fct, *fctArgs, **fctKwargs):
		"""
		Create a new actionDelay or replace an existing one.
		See game.actionDelay.ActionDelay.

		:type actionName: object
		:param actionName: The name given to the new actionDelay.

		:type waitTime: float
		:param waitTime: The time to wait before calling fct.

		:type fct: function or method
		:param fct: The function or method to delay.

		:type *fctArgs: object
		:param *fctArgs: The arguments to pass to fct.

		:type **fctKwargs: object
		:param **fctKwargs: The optional arguments to pass to the fct.
		"""

		self.actionDelays[actionName] = ActionDelay(
			waitTime, fct, *fctArgs, **fctKwargs)

	def removeActionDelay(self, *actionNames):
		"""
		Remove actionDelay(s).

		:type *actionNames: str
		:param *actionNames: The name of the actionDelays to remove.
		"""

		for actionName in actionNames:
			self.actionDelays.pop(actionName, None)

	def removeEntity(self, entity):
		"""
		Remove an Entity.

		:type entity: entities.entity.Entity
		:param entity: The entity to remove.
		"""

		if entity in self.entities:
			self.entities.remove(entity)
		else:
			print("[WARNING] [Level.removeEntity] " \
				+ "Unable to remove %s from Entity list" % entity)

	def getStyleTypeWithScore(self, score = None):
		"""
		Get the style id from the score.
		0 is normal, 1 is black and white and 2 is flashy.

		:type score: int
		:param score: Optional. A score. Use the current level score
			if undefined.

		:rtype: int
		:returns: The style id associated to the given score.
		"""

		score = score if score else self.score
		if score < 20000:
			return 0
		elif score < 30000:
			return 1
		else:
			return 2

	def getBackgroundIdWithScore(self, score = None):
		"""
		Get the background id associated to a specified score.

		:type score: int
		:param score: Optional. A score. Use the current level score
			if undefined.

		:rtype: int
		:returns: The background id associated to the given score.
		"""

		score = score if score else self.score
		if score < 11000:
			return score // 1000
		elif score < 20000:
			return 10
		elif score < 30000:
			return 11
		elif score < 40000:
			return 12
		else:
			self.createActionDelay((self, "updateAnimatedBackround"),
				BACKGROUND_ANIMATED_DURATION, self.updateAnimatedBackground)
			return self.animatedBackgroundId

	def getAudioPlayer(self):
		"""
		Get the current audio player.

		:rtype: audio.audio_player.Audio_player
		:returns: The audio player currently used by the game.
		"""
		return Game.audioPlayer

	def getVoidCases(self):
		"""
		Get the destroyed blocks that are not being repaired.

		:rtype: list<game.case.Case>
		:returns: A list of all destroyed blocks.
		"""
		return [case for case in self.cases \
			if not(case.exists) and not(case.isRepairing)]

	def setSize(self, size):
		"""
		Define the level size (in case).

		:type size: tuple
		:param size: The size in blocks of the level.
		"""

		self.size = tuple(size)
		self.initCases(int(size[0]))
