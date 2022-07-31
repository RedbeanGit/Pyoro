# -*- coding:utf-8 -*-

# 	This file is part of Pyoro (A Python fan game).
#
# 	Metawars is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	Metawars is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
Provide a base abstract class to create entities

Created on 18/03/2018
"""

import os

from game.config import ENTITIES_IMAGE_PATH
from game.util import Game
from gui.image_transformer import resize_image

__author__ = "RedbeanGit"
__version__ = "1.1.1"


class Entity:
    """
    Abstract class for all moving objects : entities
    """

    def __init__(self, level, pos, size=(1, 1)):
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
        self.current_image_name = ""

        self.init_images()
        self.init_sounds()
        self.update_sprite()

    def __repr__(self):
        """
        Represent the entity as a string.

        :rtype: str
        :returns: A string respresenting the entity.

        :Example: <Bean at pos x=2.35 y=5.86>
        """

        type_name = type(self).__name__
        return f"<{type_name} at pos x={self.pos[0]:.2f}, y={self.pos[1]:.2f}>"

    def __init_images__(self, folder_name):
        """
        Reference all images in a specific folder to use them later.
        This method should be used internally by Entity.initImages
        (see below).

        :type folder_name: str
        :param folder_name: The path to the folder where images to
            reference are.
        """

        self.images = {}
        case_size = self.level.level_drawer.get_case_size()
        image_names = os.listdir(os.path.join(ENTITIES_IMAGE_PATH, folder_name))

        for image_name in image_names:
            if image_name.split(".")[-1] == "png":
                self.images[image_name] = resize_image(
                    self.level.level_drawer.activity.window.get_image(
                        os.path.join(ENTITIES_IMAGE_PATH, folder_name, image_name)
                    ),
                    (case_size[0] * self.size[0], case_size[1] * self.size[1]),
                )
        self.update_sprite()

    def init_images(self):
        """
        Initialize the images used by the entity.
        This method should be override to refer the images of this entity.
        It's advisable to use this method with Entity.__initImages__.
        """

    def __init_sounds__(self, sound_names):
        """
        Reference sounds to use them later.
        This method should be used internally by Entity.initSounds
        (see below).

        :type sound_names: list<str>
        :param sound_names: The name of the sounds to load.
        """

        audio_player = self.level.get_audio_player()
        for sound_name in sound_names:
            self.sounds[sound_name] = audio_player.get_sound(
                os.path.join("data", "audio", "sounds", f"{sound_name}.wav")
            )

    def init_sounds(self):
        """
        Initialize the sounds used by the entity.
        This method should be override to refer the sounds of this entity.
        It's advisable to use this method with Entity.__initSounds__.
        """

    def update(self, _delta_time):
        """
        Update the entity.

        :type delta_time: float
        :param delta_time: Elapsed time since the last update (in seconds).
        """

        if self.is_out_of_bound():
            self.remove()

    def update_sprite(self):
        """
        Update the image currently used by the entity.
        This method should be override.
        """

    def is_hitting_entity(self, entity):
        """
        Check if the entity collide another.

        :type entity: entities.entity.Entity
        :param entity: An entity which is maybe colliding this one.

        :rtype: bool
        :returns: True if the entities are colliding, otherwise False.
        """

        pos = entity.pos
        size = entity.size
        return (
            (pos[0] + size[0] / 2 > self.pos[0] - self.size[0] / 2)
            and (pos[0] - size[0] / 2 < self.pos[0] + self.size[0] / 2)
            and (pos[1] + size[1] / 2 > self.pos[1] - self.size[1] / 2)
            and (pos[1] - size[1] / 2 < self.pos[1] + self.size[1] / 2)
        )

    def is_out_of_bound(self, included=True):
        """
        Check if the entity is in the terrain.

        :type included: bool
        :param included: Optional! If True (default), check if the entire
            entity is out of the terrain. Otherwise, only check if a part
            of the entity is out of bounds.

        :rtype: bool
        :returns: True if the entity is out of bounds, otherwise False.
        """

        width, height = self.level.size
        if included:
            return (
                (self.pos[0] + self.size[0] / 2 <= 0)
                or (self.pos[0] - self.size[0] / 2 >= width)
                or (self.pos[1] + self.size[1] / 2 <= 0)
                or (self.pos[1] - self.size[1] / 2 >= height)
            )
        return (
            (self.pos[0] - self.size[0] / 2 <= 0)
            or (self.pos[0] + self.size[0] / 2 >= width)
            or (self.pos[1] - self.size[1] / 2 <= 0)
            or (self.pos[1] + self.size[1] / 2 >= height)
        )

    def is_hitting_floor(self):
        """
        Check if the entity collide with the floor.

        :rtype: bool
        :returns: True if the entity is colliding the floor, otherwise False.
        """
        return self.pos[1] + self.size[1] / 2 >= self.level.size[1] - 1

    def remove(self):
        """
        Remove the entity from its level.
        The entity will no longer be updated.
        """

        self.level.remove_entity(self)
        self.remove_sounds()

    def remove_sounds(self):
        """
        Stop and remove all sounds used by this entity.
        """

        for sound in self.sounds.values():
            if sound.is_playing:
                sound.stop()
            Game.audio_player.remove_sound(sound)
