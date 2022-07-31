# -*- coding: utf-8 -*-

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
Provides an Angel class.
This entity is used to repair destroyed cases

Created on 21/03/2018
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.entity import Entity
from game.config import ANGEL_SPEED, ANGEL_SPRITE_DURATION


class Angel(Entity):
    """
    Angel that fall from the sky to repair a destroyed block
    """

    def __init__(self, level, repair_case):
        """
        Initialize an Angel object.

        :type level: game.level.Level
        :param level: The level managing this entity

        :type repair_case: game.case.Case
        :param repair_case: The block to repair
        """

        self.sprite_index = 0
        self.case = repair_case
        self.case.is_repairing = True
        Entity.__init__(self, level, (repair_case.pos + 0.75, 0.75), (1.5, 1.5))

    def init_images(self):
        """
        Load angel images.
        """

        self.__init_images__("angel")

    def init_sounds(self):
        """
        Load angel sounds and start playing a falling sound.
        """

        self.__init_sounds__(("angel_down",))
        self.sounds["angel_down"].play()

    def update(self, delta_time):
        """
        Update the angel (position, sprite).

        :type delta_time: float
        :param delta_time: Time elapsed since the last frame update
        """

        if self.case.is_repairing:
            self.pos[1] += ANGEL_SPEED * delta_time
        else:
            self.pos[1] -= ANGEL_SPEED * delta_time
        if self.is_hitting_floor():
            self.repair_case()
        Entity.update(self, delta_time)

    def repair_case(self, case=None):
        """
        Repair a destroyed block.

        :type case: game.case.Case
        :param case: The block to repair.
                Leave None to repair the default block.
        """

        case = case if case else self.case
        case.is_repairing = False
        case.exists = True
        self.sounds["angel_down"].stop()

    def update_sprite(self):
        """
        Update the images to create a flight animation.
        """

        score = self.level.get_style_type_with_score()
        self.sprite_index = 1 if self.sprite_index == 0 else 0
        self.current_image_name = f"angel_{score}_{self.sprite_index}.png"
        self.level.set_action_delay(
            (self, "updateSprite"), ANGEL_SPRITE_DURATION, self.update_sprite
        )

    def remove(self):
        """
        Remove the angel from its level and stop all actions delayed.
        """

        self.level.remove_action_delay((self, "updateSprite"))
        Entity.remove(self)
