# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 27/03/2018
	@version: 1
=========================
"""

import os, math

from entities.entity import Entity
from gui.image_transformer import Image_transformer
from game.config import SEED_SPEED, AIR_RESISTANCE, GRAVITY_FORCE, ENTITIES_IMAGE_PATH, WIDTH, HEIGHT, CASE_SIZE

class Seed(Entity):
	def __init__(self, level, angle, direction):
		self.direction = direction
		self.spriteAlpha = 255
		self.vel = [
			math.cos(angle * math.pi / 180) * direction * SEED_SPEED,
			-math.sin(angle * math.pi / 180) * SEED_SPEED
		]
		
		pos = (level.pyoro.pos[0] + (level.pyoro.size[0] / 2 + 0.0625) * direction, 
			level.pyoro.pos[1] - level.pyoro.size[1] / 2 + 0.0625)
		
		Entity.__init__(self, level, pos, (0.125, 0.125))

	def __initImages__(self, folderName):
		self.images = {}
		folder = os.path.join(ENTITIES_IMAGE_PATH, folderName)
		imageNames = os.listdir(folder)
		for imageName in imageNames:
			if imageName.split(".")[-1] == "png":
				self.images[imageName] = Image_transformer.resize(
					self.level.activity.window.getImage(
						os.path.join(folder, imageName), 
						alphaChannel = False), \
					(CASE_SIZE * self.size[0], CASE_SIZE * self.size[1]))
				self.images[imageName].set_alpha(self.spriteAlpha)
				self.currentImageName = imageName
	
	def initImages(self):
		self.__initImages__("seed")
	
	def update(self, deltaTime):
		self.vel[0] -= AIR_RESISTANCE * self.direction * deltaTime
		self.vel[1] += GRAVITY_FORCE * deltaTime
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]
		
		if self.spriteAlpha > 0:
			self.spriteAlpha -= 64 * deltaTime
		else:
			self.remove()
		Entity.update(self, deltaTime)

	def updateSprite(self):
		self.currentImageName = "seed_{}.png".format(self.level.getStyleTypeWithScore())
		self.images[self.currentImageName].set_alpha(self.spriteAlpha)