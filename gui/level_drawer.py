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
Provide a class to draw a game.level.Level and entities.entity.Entity

Created on 11/10/2018
"""

import os
import pygame

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import CASE_SIZE, BACKGROUND_TRANSITION_DURATION, \
	LEVEL_IMAGE_PATH
from game.level import Level
from game.util import getMonitorSize, getScreenSize, getMonitorDensity
from gui.image_transformer import resizeImage


class Level_drawer:
	"""
	Create a Level_drawer object, usually used to draw a level and its
		entities on the screen.
	"""

	def __init__(self, activity, gameId, botMode=False):
		"""
		Initialize a new Level_drawer object, create a new level and load
			background images.

		:type activity: gui.activity.Activity
		:param activity: The parent activity where to draw the level.

		:type gameId: int
		:param gameId: An integer representing Pyoro 1 or 2 (0=Pyoro,
			1=Pyoro 2).

		:type botMode: bool
		:param botMode: (Optional) Define if Pyoro have to be replaced by
			Pyobot. Default is False.
		"""

		self.activity = activity
		self.images = {}
		self.caseSize = ()
		self.level = None

		self.initLevel(gameId, botMode)

		self.lastBackgroundId = self.level.getBackgroundIdWithScore()
		self.lastBackground = None

		self.initImages()

	def initLevel(self, gameId, botMode):
		"""
		Create a new level with given gameId and botMode value.

		:type gameId: int
		:param gameId: An integer representing Pyoro 1 or 2 (0=Pyoro,
			1=Pyoro 2).

		:type botMode: bool
		:param botMode: Define if Pyoro have to be replaced by Pyobot. Default
			is False.
		"""

		self.level = Level(self, gameId, self.getLevelSize(), botMode)

	def getLevelSize(self):
		"""
		Return the size of the level (the scale is expressed in case).

		:rtype: tuple
		:returns: A (w, h) tuple where w is an integer and h is a float
			number.
		"""

		wp, hp = getScreenSize()
		wd, hd = getMonitorDensity()
		wc, hc = wd * CASE_SIZE, hd * CASE_SIZE
		return int(wp / wc), hp / hc

	def getCaseSize(self):
		"""
		Return the size of one case in pixel.

		
		:rtype: tuple
		:returns: A (w, h) tuple where w and h are both float numbers.
		"""

		if not self.caseSize:
			wp, hp = getScreenSize()
			if self.level:
				wc, hc = self.level.size
			else:
				wc, hc = self.getLevelSize()
			self.caseSize = wp / wc, hp / hc
		return self.caseSize

	def initImages(self):
		"""
		Initialize background images.
		"""

		folder = os.path.join(LEVEL_IMAGE_PATH, "block")
		size = self.getCaseSize()
		for i in range(3):
			imageName = "block_%s.png" % i
			self.images[imageName] = resizeImage(
				self.activity.window.getImage(os.path.join(folder, imageName)), \
				size)

		folder = os.path.join(LEVEL_IMAGE_PATH, \
			"background %s" % (self.level.gameId + 1))
		size = self.activity.window.getSize()
		for i in range(21):
			imageName = "background_%s.png" % i
			self.images[imageName] = resizeImage(
				self.activity.window.getImage(os.path.join(folder, imageName), \
				alphaChannel = False), size)

	def drawPyoro(self):
		"""
		Draw Pyoro (or Pyoro 2) and its tongue when he tries to catch a bean.
		"""

		p = self.level.pyoro
		t = p.tongue
		caseSize = self.getCaseSize()
		if t:
			# define tongue colors (insideColor, outlineColor)
			styleType = self.level.getStyleTypeWithScore()
			if styleType == 0:
				color = ((255, 98, 183), (0, 0, 0))
			elif styleType == 1:
				color = ((178, 178, 178), (0, 0, 0))
			else:
				color = ((0, 0, 0), (255, 255, 255))

			# define tongue pos
			tx1 = t.pos[0] - t.size[0] * 0.5 * p.direction
			tx2 = t.pos[0] - t.size[0] * 0.4 * p.direction
			px1 = p.pos[0] + p.size[0] * 0.25 * p.direction
			px2 = p.pos[0] + p.size[0] * 0.3125 * p.direction

			ty1 = t.pos[1] + t.size[1] * 0.4
			ty2 = t.pos[1] + t.size[1] * 0.5
			py1 = p.pos[1] - p.size[1] * 0.125
			py2 = p.pos[1] - p.size[1] * 0.0625

			tCoords = [(px1, py1), (tx1, ty1), (tx2, ty2), (px2, py2)]

			for key, pos in enumerate(tCoords):
				x = int(pos[0] * self.caseSize[0] + 5)
				y = int(pos[1] * self.caseSize[1] + 5)
				tCoords[key] = (x, y)

			pygame.draw.polygon(self.activity.window.rootSurface, color[0], tCoords)
			pygame.draw.line(self.activity.window.rootSurface, color[1],
				tCoords[0], tCoords[1], int(0.115 * caseSize[0]))
			pygame.draw.line(self.activity.window.rootSurface, color[1],
				tCoords[2], tCoords[3], int(3.68))

		self.activity.window.drawImage(p.images[p.currentImageName],
			((p.pos[0] - p.size[0] / 2) * caseSize[0],
				(p.pos[1] - p.size[1] / 2) * caseSize[1]))

	def drawBackground(self):
		"""
		Draw the appropriate background image by handling smooth transition
			animations between different background images.
		"""

		backId = self.level.getBackgroundIdWithScore()
		background = self.images["background_%s.png" % backId]

		if backId == 0:
			background.set_alpha(255)
		else:
			if self.lastBackgroundId != backId:
				self.lastBackground = self.images[
					"background_%s.png" % self.lastBackgroundId]
				self.lastBackgroundId = backId

				self.lastBackground.set_alpha(255)
				background.set_alpha(0)

				self.updateBackgroundTransition(0)
			self.activity.window.drawImage(self.lastBackground, (0, 0))
		self.activity.window.drawImage(background, (0, 0))

	def drawBlocks(self):
		"""
		Draw the cases which are not destroyed.
		"""

		w, h = self.activity.window.getSize()
		caseSize = self.getCaseSize()
		for i in range(self.level.size[0]):
			if self.level.cases[i].exists:
				self.activity.window.drawImage(self.images[
					"block_%s.png" % self.level.getStyleTypeWithScore()],
					(i * caseSize[0], h - caseSize[1]))

	def updateBackgroundTransition(self, opacity):
		"""
		Increase new background opacity to create a smooth transition
			animation.

		:type opacity: float
		:param opacity: Opacity of the new background image (1 <= opacity 
			<= 255).
		"""

		self.images["background_%s.png" \
			% self.level.getBackgroundIdWithScore()].set_alpha(opacity)

		if opacity < 255:
			self.level.setActionDelay((self, "updateBackgroundTransition"),
				BACKGROUND_TRANSITION_DURATION / 128,
				self.updateBackgroundTransition, opacity + 2)
		else:
			self.level.removeActionDelay((self, "updateBackgroundTransition"))

	def drawEntities(self):
		"""
		Draw all entities stored in the level except Pyoro (There is another
			method to draw Pyoro).
		"""

		w, h = self.getCaseSize()
		for entity in self.level.entities:
			x = (entity.pos[0] - entity.size[0] / 2) * w
			y = (entity.pos[1] - entity.size[1] / 2) * h
			self.activity.window.drawImage(entity.images[entity.currentImageName],
				(x, y))

	def update(self, deltaTime):
		"""
		Update the level drawer by drawing background, blocks, Pyoro and
			entities images.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last update.
		"""

		self.level.update(deltaTime)
		self.drawBackground()
		self.drawBlocks()
		self.drawPyoro()
		self.drawEntities()
