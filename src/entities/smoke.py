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
Provide a Smoke class for destruction animations.

Created on 21/03/2018.
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.entity import Entity
from game.config import SMOKE_SPRITE_DURATION


class Smoke(Entity):
    """
    Create a Smoke object used for destrution animations.
    """

    def __init__(self, level, pos):
        """
        Initialize a new Smoke object.

        :type level: game.level.Level
        :param level: The level managing this entity.

        :type pos: list
        :param pos: An [x, y] list where x and y are both float numbers.
        """

        self.sprite_index = 0
        Entity.__init__(self, level, pos, (1.5, 1.5))

    def init_images(self):
        """
        Initialize smoke images.
        """

        self.__init_images__("smoke")

    def update(self, deltaTime):
        """
        Update the smoke.

        :type deltaTime: float
        :param deltaTime: Time elapsed since the last update.
        """

        self.level.createActionDelay((self, "destroy"),
                                     SMOKE_SPRITE_DURATION * 3, self.remove)
        Entity.update(self, deltaTime)

    def update_sprite(self):
        """
        Define the sprite to use according to the animation's state and the
            current level style.
        """

        score = self.level.getStyleTypeWithScore()
        self.sprite_index = self.sprite_index + 1 if self.sprite_index < 2 else 0
        self.current_image_name = f"smoke_{score}_{self.sprite_index}.png"

        self.level.setActionDelay((self, "update_sprite"),
                                  SMOKE_SPRITE_DURATION, self.update_sprite)

    def remove(self):
        """
        Remove the smoke actions delayed and the smoke itself.
        """

        self.level.removeActionDelay(
            (self, "destroy"), (self, "update_sprite"))
        Entity.remove(self)
