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
Provide a Score_text class (entity).

Created on 21/03/2018.
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.entity import Entity
from game.config import SCORE_TEXT_BLINK_DURATION, SCORE_TEXT_LIFE_DURATION


class ScoreText(Entity):
    """
    Create a Score_text which is a flashy entity to show points that has just
        been earned at a specific position.
    """

    def __init__(self, level, pos, value):
        """
        Initialize a new Score_text object.

        :type level: game.level.Level
        :param level: The level managing this entity.

        :type pos: list
        :param pos: An [x, y] list where x and y are both float numbers.

        :type value: int
        :param value: The value to display (it can be 10, 50, 100, 300 or
            1000).
        """

        pixel_size = 1
        for _ in str(value):
            if value == 1:
                pixel_size += 2
            else:
                pixel_size += 4
        self.value = value
        self.color_index = 0
        Entity.__init__(self, level, pos, (pixel_size * 0.125, 0.875))

    def init_images(self):
        """
        Initialize score_text images.
        """

        self.__init_images__("score text")

    def update(self, deltaTime):
        """
        Update the score_text.

        :type deltaTime: float
        :param deltaTime: Time elapsed since the last update.
        """

        self.level.createActionDelay(
            (self, "destroy"), SCORE_TEXT_LIFE_DURATION, self.remove)
        Entity.update(self, deltaTime)

    def update_sprite(self):
        """
        Change the sprite to make a blinking effect.
        """

        if self.value in (300, 1000):
            self.color_index = self.color_index + 1 if self.color_index < 5 else 0
            self.current_image_name = f"number_{self.value}_{self.color_index}.png"
        else:
            self.current_image_name = f"number_{self.value}.png"
        self.level.setActionDelay(
            (self, "update_sprite"), SCORE_TEXT_BLINK_DURATION, self.update_sprite)

    def remove(self):
        """
        Remove the score_text actions delayed en the score_text itself.
        """

        self.level.removeActionDelay(
            (self, "destroy"), (self, "update_sprite"))
        Entity.remove(self)
