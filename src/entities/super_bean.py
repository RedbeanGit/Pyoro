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
Provide a Score_text class (entity).

Created on 17/03/2018.
"""

import random

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.bean import Bean
from game.config import BEAN_SPRITE_DURATION


class SuperBean(Bean):
    """
    Create a Super_bean object which have the hability to repair 10 destroyed
        cases and to explode all beans currently falling.
    """

    def __init__(self, level, pos, speed):
        """
        Initialize a new Super_bean object.

        :type level: game.level.Level
        :param level: The level managing this entity.

        :type pos: list
        :param pos: An [x, y] list where x and y are both float numbers.

        :type speed: float
        :param speed: The falling speed multiplicator.
        """

        self.sprite_index = 0
        self.color_index = 0
        Bean.__init__(self, level, pos, speed)

    def init_images(self):
        """
        Initialize super_bean images.
        """

        self.__init_images__("super bean")

    def init_sounds(self):
        """
        Load super_bean sounds.
        """

        Bean.init_sounds(self)
        self.__init_sounds__(("bean_implode",))

    def update_sprite(self):
        """
        Define the sprite to use according to the blinking animation state and
            the current level style.
        """

        if not self.color_index % 2:
            self.sprite_index = self.sprite_index + 1 if self.sprite_index < 2 else 0

        self.color_index = self.color_index + 1 if self.color_index < 5 else 0
        self.current_image_name = f"bean_{self.sprite_index}_{self.color_index}.png"

        self.level.set_action_delay(
            (self, "update_sprite"), BEAN_SPRITE_DURATION / 6, self.update_sprite
        )

    def catch(self):
        """
        Explode all the beans currently falling and repair 10 destroyed cases.
        """

        i = 0
        for entity in self.level.entities:
            if isinstance(entity, Bean) and entity != self:
                self.level.create_action_delay(
                    (self, "destroy_bean", i), i * 0.1, self.destroy_bean, entity, i
                )
                i += 1
        i = 0
        empty_cases = list(self.level.get_void_cases())
        for i in range(min(10, len(empty_cases))):
            self.level.create_action_delay(
                (self, "repair_case", empty_cases[i].pos),
                i * 0.5,
                self.repair_case,
                empty_cases[i],
            )
        Bean.catch(self)

    def destroy_bean(self, bean, bean_id):
        """
        Explode a bean, increase the score and remove action delayed
            associated with this bean.

        :type bean: entities.bean.Bean
        :param bean: The bean to destroy.

        :type bean_id: int
        :param bean_id: An integer associated with this bean when the explosion
            was decided.
        """

        self.sounds["bean_implode"].play()
        bean.cut()
        bean.remove()
        self.level.spawn_score(50, bean.pos)
        self.level.remove_action_delay((self, "destroy_bean", bean_id))

    def cut(self):
        """
        Spawn super leafs and play a sound.
        """

        self.sounds["bean_cut"].play()
        for _ in range(2):
            rand_pos = [
                self.pos[0] + random.uniform(-0.5, 0.5),
                self.pos[1] + random.uniform(-0.5, 0.2),
            ]
            self.level.spawn_leaf(rand_pos, "super leaf")

    def repair_case(self, case):
        """
        Repair a case and remove the associated action delayed.

        :type case: game.case.Case
        :param case: The case to repair.
        """

        self.level.repair_case(case)
        self.level.remove_action_delay((self, "repair_case", case.pos))

    def remove(self):
        """
        Remove the super bean action delayed and the super bean itself.
        """

        self.level.remove_action_delay(("override", self, "update_sprite"))
        Bean.remove(self)
