# -*- coding:utf-8 -*-

"""
Provide a base abstract class to create entities

Created on 18/03/2018
"""

from game.config import CASE_SIZE, ENTITIES_IMAGE_PATH
from gui.image_transformer import Image_transformer

__author__ = "Julien Dubois"
__version__ = "1.1.1"

import os


class Entity:
	"""
	Abstract class for all moving objects : entities
	"""

	def __init__(self, level, pos, size = (1, 1)):
		"""
		Initialize an Entity object.

		:type level: game.level.Level
		:param level: The level managing this entity.

		:type pos: list<float>
		:param pos: The default (x, y) position of the entity.

		:type size: list<float>
		:param size: Optional! The (width, height) size of the entity.
			Default is [1, 1].
		"""

		self.level = level

		self.size = list(size)
		self.pos = list(pos)
		self.sounds = {}
		self.images = {}
		self.currentImageName = ""

		self.initImages()
		self.initSounds()
		self.updateSprite()

	def __repr__(self):
		"""
		Represent the entity as a string.

		:rtype: str
		:returns: A string respresenting the entity.

		:Example: <Bean at pos x=2.35 y=5.86>
		"""

		return "<{} at pos x={:.2f}, y={:.2f}>".format(
			type(self).__name__, *self.pos)

	def __initImages__(self, folderName):
		"""
		Reference all images in a specific folder to use them later.
		This method should be used internally by Entity.initImages
		(see below).

		:type folderName: str
		:param folderName: The path to the folder where images to
			reference are.
		"""

		self.images = {}
		imageNames = os.listdir(os.path.join(ENTITIES_IMAGE_PATH, folderName))
		for imageName in imageNames:
			if imageName.split(".")[-1] == "png":
				self.images[imageName] = Image_transformer.resize(
					self.level.activity.window.getImage(
						os.path.join(ENTITIES_IMAGE_PATH,
							folderName, imageName)), \
					(CASE_SIZE * self.size[0], CASE_SIZE * self.size[1]))
		self.updateSprite()

	def initImages(self):
		"""
		Initialize the images used by the entity.
		This method should be override to refer the images of this entity.
		It's advisable to use this method with Entity.__initImages__.
		"""
		pass

	def __initSounds__(self, soundNames):
		"""
		Reference sounds to use them later.
		This method should be used internally by Entity.initSounds
		(see below).

		:type soundNames: list<str>
		:param soundNames: The name of the sounds to load.
		"""

		ap = self.level.getAudioPlayer()
		for soundName in soundNames:
			self.sounds[soundName] = ap.getSound(os.path.join(
				"data", "audio", "sounds", "{}.wav".format(soundName)))

	def initSounds(self):
		"""
		Initialize the sounds used by the entity.
		This method should be override to refer the sounds of this entity.
		It's advisable to use this method with Entity.__initSounds__.
		"""
		pass

	def update(self, deltaTime):
		"""
		Update the entity.

		:type deltaTime: float
		:param deltaTime: Elapsed time since the last update (in seconds).
		"""

		if self.isOutOfBounds():
			self.remove()

	def updateSprite(self):
		"""
		Update the image currently used by the entity.
		This method should be override.
		"""
		pass

	def isHittingEntity(self, entity):
		"""
		Check if the entity collide another.

		:type entity: entities.entity.Entity
		:param entity: An entity which is maybe colliding this one.

		:rtype: bool
		:returns: True if the entities are colliding, otherwise False.
		"""

		p = entity.pos
		s = entity.size
		return (p[0] + s[0] / 2 > self.pos[0] - self.size[0] / 2) \
		   and (p[0] - s[0] / 2 < self.pos[0] + self.size[0] / 2) \
		   and (p[1] + s[1] / 2 > self.pos[1] - self.size[1] / 2) \
		   and (p[1] - s[1] / 2 < self.pos[1] + self.size[1] / 2)

	def isOutOfBounds(self, included = True):
		"""
		Check if the entity is in the terrain.

		:type included: bool
		:param included: Optional! If True (default), check if the entire
			entity is out of the terrain. Otherwise, only check if a part
			of the entity is out of bounds.

		:rtype: bool
		:returns: True if the entity is out of bounds, otherwise False.
		"""

		w, h = self.level.getSize()
		if included:
			return (self.pos[0] + self.size[0] / 2 <= 0) \
				or (self.pos[0] - self.size[0] / 2 \
				>= w) \
				or (self.pos[1] + self.size[1] / 2 <= 0) \
				or (self.pos[1] - self.size[1] / 2 \
				>= h)
		else:
			return (self.pos[0] - self.size[0] / 2 <= 0) \
				or (self.pos[0] + self.size[0] / 2 \
				>= w) \
				or (self.pos[1] - self.size[1] / 2 <= 0) \
				or (self.pos[1] + self.size[1] / 2 \
				>= h)

	def isHittingTheFloor(self):
		"""
		Check if the entity collide with the floor.

		:rtype: bool
		:returns: True if the entity is colliding the floor, otherwise False.
		"""
		return self.pos[1] + self.size[1] / 2 >= self.level.getSize()[1] - 1

	def remove(self):
		"""
		Remove the entity from its level.
		The entity will no longer be updated.
		"""

		self.level.removeEntity(self)
		self.stopSounds()

	def stopSounds(self):
		"""
		Stop all sounds used by the entity.
		"""

		for sound in self.sounds.values():
			if sound.isPlaying:
				sound.stop()
