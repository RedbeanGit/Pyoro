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
Provides a Leaf class.
This entity is used as leaf particles when a bean is destroyed.

Created on 07/05/2018
"""

import random

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import LEAF_SPEED, LEAF_SPRITE_DURATION, LEAF_WIND_SPEED, \
    AIR_RESISTANCE
from entities.entity import Entity


class Leaf(Entity):
    """
    Define a leaf which appears when a bean is destroyed. There are 3 leaf
        types ("leaf", "pink leaf" and "super leaf") depending on the bean
        that has just been destroyed.
    """

    def __init__(self, level, pos, speed, leaf_type):
        """
        Initialise a Leaf object.

        :type level: game.level.Level
        :param level: The level managing this entity.

        :type pos: list
        :param pos: The default position of the leaf in a [x, y] list where x
            and y are both float numbers.

        :type speed: float
        :param speed: The falling speed of the leaf.

        :type leaf_type: str
        :param leaf_type: The type of the leaf. It can be "leaf", "pink leaf"
            or "super leaf".
        """

        self.vel = 0
        self.sprite_index = 0
        self.leaf_type = leaf_type
        self.speed = speed
        Entity.__init__(self, level, pos, (0.75, 0.75))

    def init_images(self):
        """
        Load leaf images.
        """

        self.__init_images__(self.leaf_type)

    def update(self, deltaTime):
        """
        Update the leaf (position, sprite).

        :type deltaTime: float
        :param deltaTime: Time elapsed since the last frame update
        """

        self.pos[0] += self.vel * deltaTime
        self.pos[1] += (LEAF_SPEED - abs(self.vel)) * self.speed * deltaTime
        if self.vel > 0:
            self.vel -= AIR_RESISTANCE * deltaTime
            if self.vel < 0:
                self.vel = 0
        elif self.vel < 0:
            self.vel += AIR_RESISTANCE * deltaTime
            if self.vel > 0:
                self.vel = 0
        Entity.update(self, deltaTime)

    def update_sprite(self):
        """
        Update the images to create a flight animation.
        """

        score = self.level.get_style_with_score()
        self.sprite_index = self.sprite_index + 1 if self.sprite_index < 2 else 0
        self.current_image_name = f"leaf_{score}_{self.sprite_index}.png"

        self.level.set_action_delay((self, "updateSprite"),
                                    LEAF_SPRITE_DURATION, self.update_sprite)

    def set_left_wind(self):
        """
        Change the leaf's velocity as if there is wind to the left.
        """

        self.vel = -LEAF_WIND_SPEED

    def set_right_wind(self):
        """
        Change the leaf's velocity as if there is wind to the right.
        """

        self.vel = LEAF_WIND_SPEED

    def cut(self):
        """
        Replace the leaf by 2 leaf pieces as if it was cut in a half.
        """

        if not random.randint(0, 2):
            for delta_pos in (-self.size[0], self.size[0]):
                self.level.spawn_leaf_piece((self.pos[0] + delta_pos / 2,
                                             self.pos[1]), self.speed, self.leaf_type + " piece",
                                            self.vel / 2)
            self.remove()

    def remove(self):
        """
        Remove the leaf and its action delayed.
        """

        self.level.remove_action_delay((self, "updateSprite"))
        Entity.remove(self)
