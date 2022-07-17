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
Provide a Tongue class.

Created on 21/03/2018.
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.bean import Bean
from entities.entity import Entity
from game.config import TONG_SPEED


class Tongue(Entity):
    """
    Creat a Tongue object used by Pyoro to catch falling beans.
    """

    def __init__(self, level, direction):
        """
        Initialize a new Tongue object.

        :type level: game.level.Level
        :param level: The level managing this entity.

        :type direction: int
        :param direction: The direction of the tongue (1 = right, -1 = left).
        """

        self.direction = direction
        self.caught_bean = None
        self.go_back = False

        pos = (level.pyoro.pos[0] + (level.pyoro.size[0] / 2 + 0.6) * direction,
               level.pyoro.pos[1] - level.pyoro.size[1] / 2 + 0.6)

        Entity.__init__(self, level, pos, (1.2, 1.2))

    def init_images(self):
        """
        Initialize tongue images.
        """

        self.__init_images__("tongue")

    def init_sounds(self):
        """
        Load tongue sounds.
        """

        self.__init_sounds__(("tongue", "pyoro_eat"))
        self.sounds["tongue"].play()

    def update(self, deltaTime):
        """
        Update the tongue (position, direction, ...).

        :type deltaTime: float
        :param deltaTime: Time elapsed since the last update.
        """

        _, height = self.level.size
        if self.go_back:
            self.pos[0] -= TONG_SPEED * 2 * self.direction * deltaTime
            self.pos[1] += TONG_SPEED * 2 * deltaTime

            if self.caught_bean:
                self.caught_bean.pos[0] -= TONG_SPEED * \
                    2 * self.direction * deltaTime
                self.caught_bean.pos[1] += TONG_SPEED * 2 * deltaTime

            if self.pos[1] >= self.level.pyoro.pos[1]:
                if self.caught_bean:
                    self.sounds["pyoro_eat"].play()
                    self.level.pyoro.eatingCount = 1
                self.remove()
        else:
            self.pos[0] += TONG_SPEED * self.direction * deltaTime
            self.pos[1] -= TONG_SPEED * deltaTime

            for entity in self.level.entities:
                if self.is_hitting_entity(entity) and isinstance(entity, Bean):
                    entity.catch()
                    self.sounds["tongue"].stop()

                    _, height = self.level.size
                    if self.pos[1] < height * 0.2:
                        score = 1000
                    elif self.pos[1] < height * 0.4:
                        score = 300
                    elif self.pos[1] < height * 0.6:
                        score = 100
                    elif self.pos[1] < height * 0.8:
                        score = 50
                    else:
                        score = 10
                    self.level.spawnScore(score, self.pos)
                    self.caught_bean = entity
                    self.go_back = True
                    return None
            self.go_back = self.is_out_of_bound(False)
        self.update_sprite()
        Entity.update(self, deltaTime)

    def update_sprite(self):
        """
        Define the sprite to use according to the current level style.
        """

        score = self.level.getSTyleTypeWithScore()
        self.current_image_name = f"tongue_{score}_{self.direction}.png"

    def remove(self):
        """
        Remove the caught bean and the tongue itself.
        """

        if self.caught_bean:
            self.caught_bean.remove()
        self.level.pyoro.tongue = None
        Entity.remove(self)
