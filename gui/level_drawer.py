# -*- coding: utf-8 -*-

"""
Provide a class to draw a game.level.Level and entities.entity.Entity

Created on 11/10/2018
"""

from game.config import CASE_SIZE, \
	BACKGROUND_TRANSITION_DURATION, LEVEL_IMAGE_PATH
from gui.image_transformer import Image_transformer

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import os
import pygame


class Level_drawer:
	def __init__(self, level, window):
		self.level = level
		self.window = window
		self.images = {}
		self.lastBackgroundId = self.level.getBackgroundIdWithScore()
		self.lastBackground = None

	def initImages(self):
		for i in range(2):
			if i:
				folder = os.path.join(LEVEL_IMAGE_PATH, "block")
			else:
				folder = os.path.join(LEVEL_IMAGE_PATH, "background {}".format(self.level.gameId + 1))
			imageNames = os.listdir(folder)
			for imageName in imageNames:
				if imageName.split(".")[-1] == "png":
					if i:
						self.images[imageName] = Image_transformer.resize(
							self.window.getImage(os.path.join(folder, imageName)),
							(CASE_SIZE, CASE_SIZE))
					else:
						self.images[imageName] = Image_transformer.resize(
							self.window.getImage(os.path.join(folder, imageName), alphaChannel = False),
							self.window.getSize())
					self.images[imageName].set_alpha(0)

	def getNbCases(self):
		ww, wh = self.window.getSize()
		return ww // CASE_SIZE

	def drawPyoro(self):
		p = self.level.pyoro
		t = p.tong
		if t:
			# define tong colors (insideColor, outlineColor)
			styleType = self.level.getStyleTypeWithScore()
			if styleType == 0:
				color = ((255, 98, 183), (0, 0, 0))
			elif styleType == 1:
				color = ((178, 178, 178), (0, 0, 0))
			else:
				color = ((0, 0, 0), (255, 255, 255))

			# define tong pos
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
				x = int(pos[0] * CASE_SIZE + 5)
				y = int(pos[1] * CASE_SIZE + 5)
				tCoords[key] = (x, y)

			pygame.draw.polygon(self.window.root_window, color[0], tCoords)
			pygame.draw.line(self.window.root_window, color[1],
				tCoords[0], tCoords[1], int(0.115 * CASE_SIZE))
			pygame.draw.line(self.window.root_window, color[1],
				tCoords[2], tCoords[3], int(3.68))
		self.window.drawImage(p.images[p.currentImageName],
			((p.pos[0] - p.size[0] / 2) * CASE_SIZE,
				(p.pos[1] - p.size[1] / 2) * CASE_SIZE))

	def drawBackground(self):
		backId = self.level.getBackgroundIdWithScore()
		background = self.images["background_{}.png".format(backId)]

		if backId == 0:
			background.set_alpha(255)
		else:
			if self.lastBackgroundId != backId:
				self.lastBackground = self.images["background_{}.png".format(self.lastBackgroundId)]
				self.lastBackgroundId = backId

				self.lastBackground.set_alpha(255)
				background.set_alpha(0)

				self.updateBackgroundTransition(0)
			self.window.drawImage(self.lastBackground, (0, 0))
		self.window.drawImage(background, (0, 0))

	def drawBlocks(self):
		w, h = self.level.getSize()
		for i in range(w):
			if self.level.cases[i].exists:
				self.window.drawImage(self.images["block_%s.png" \
					% self.level.getStyleTypeWithScore()],
					(i * CASE_SIZE, (h - 1) * CASE_SIZE))

	def updateBackgroundTransition(self, opacity):
		self.images["background_%s.png" \
			% self.level.getBackgroundIdWithScore()].set_alpha(opacity)

		if opacity < 255:
			self.level.setActionDelay((self, "updateBackgroundTransition"),
				BACKGROUND_TRANSITION_DURATION / 128,
				self.updateBackgroundTransition, opacity + 2)
		else:
			self.level.removeActionDelay((self, "updateBackgroundTransition"))

	def drawEntities(self):
		for entity in self.level.entities:
			x = (entity.pos[0] - entity.size[0] / 2) * CASE_SIZE
			y = (entity.pos[1] - entity.size[1] / 2) * CASE_SIZE
			self.window.drawImage(entity.images[entity.currentImageName],
				(x, y))

	def update(self, deltaTime):
		self.drawBackground()
		self.drawBlocks()
		self.drawPyoro()
		self.drawEntities()
