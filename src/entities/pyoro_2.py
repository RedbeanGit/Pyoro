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
Provide a Pyoro class, the main character of the game.

Created on 18/03/2018.
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.bean import Bean
from entities.leaf import Leaf
from entities.pyoro import Pyoro
from entities.seed import Seed
from game.config import PYORO_SHOOT_SPRITE_DURATION


class Pyoro2(Pyoro):
    """
    Create a Pyoro 2 (a little yellow bird) controlled by the player in game.
    """

    def __init__(self, level):
        """
        Initialize a new Pyoro 2 object.

        :type level: game.level.Level
        :param level: The level managing this entity.
        """

        self.shoot_sprite_id = 0
        Pyoro.__init__(self, level)

    def init_images(self):
        """
        Initialize Pyoro 2 images.
        """

        self.__init_images__("pyoro 2")

    def init_sounds(self):
        """
        Load Pyoro 2 sounds.
        """

        self.__init_sounds__(("pyoro_shoot",))
        Pyoro.init_sounds(self)

    def enable_move_left(self):
        """
        Make Pyoro 2 move to the left by defining its direction.
        """

        if self.shoot_sprite_id:
            self.shoot_sprite_id = 0
            self.level.removeActionDelay((self, "update_shoot_sprite_id"))
        Pyoro.enable_move_left(self)

    def enable_move_right(self):
        """
        Make Pyoro 2 move to the right by defining its direction.
        """

        if self.shoot_sprite_id:
            self.shoot_sprite_id = 0
            self.level.removeActionDelay((self, "update_shoot_sprite_id"))
        Pyoro.enable_move_right(self)

    def update(self, delta_time):
        """
        Update Pyoro 2 (position, posture and sprite).

        :type delta_time: float
        :param delta_time: Time elapsed since the last update.
        """

        if self.shoot_sprite_id == 1:
            self.level.createActionDelay((self, "update_shoot_sprite_id"),
                                         PYORO_SHOOT_SPRITE_DURATION, self.update_shoot_sprite_id)
        Pyoro.update(self, delta_time)

    def update_shoot_sprite_id(self):
        """
        Update shoot sprite index value for shoot animations.
        """

        self.shoot_sprite_id += 1
        if self.shoot_sprite_id < 5:
            self.level.setActionDelay((self, "update_shoot_sprite_id"),
                                      PYORO_SHOOT_SPRITE_DURATION, self.update_shoot_sprite_id)
        else:
            self.shoot_sprite_id = 0
            self.level.removeActionDelay((self, "update_shoot_sprite_id"))

    def update_sprite(self):
        """
        Define the sprite to use (normal, shooting, jumping, dying)
        """

        style_type = self.level.get_style_type_with_score()
        shoot_type = self.shoot_sprite_id - 1
        if self.dead:
            self.current_image_name = f"pyoro_{style_type}_die_{self.directio}.png"
        elif self.shoot_sprite_id:
            self.current_image_name = f"pyoro_{style_type}_shoot_{shoot_type}_{self.direction}.png"
        elif self.notch:
            self.current_image_name = f"pyoro_{style_type}_jump_{self.direction}.png"
        else:
            self.current_image_name = f"pyoro_{style_type}_normal_{self.direction}.png"

    def enable_capacity(self):
        """
        Stop Pyoro 2 and make him cut some beans and leafs.
        """

        self.sounds["pyoro_shoot"].play()
        self.shoot_sprite_id = 1
        bean_coords = []

        for entity in self.level.entities:
            if self.is_shooting_entity(entity):
                if isinstance(entity, Bean):
                    entity.cut()
                    entity.catch()
                    entity.remove()
                    bean_coords.append(list(entity.pos))
                elif isinstance(entity, Leaf):
                    entity.cut()
                    if self.direction == 1:
                        entity.setRightWind()
                    else:
                        entity.setLeftWind()

        if len(bean_coords) == 1:
            score = 50
        elif len(bean_coords) == 2:
            score = 100
        elif len(bean_coords) == 3:
            score = 300
        else:
            score = 1000

        for bean_pos in bean_coords:
            self.level.spawnScore(score, bean_pos)
        self.level.entities.append(Seed(self.level, 35, self.direction))
        self.level.entities.append(Seed(self.level, 55, self.direction))

    def is_shooting_entity(self, entity):
        """
        Return True if entity is on the trajectory of a potential shot.

        :rtype: bool
        :returns: True if Pyoro 2 can shoot the entity, False otherwise.
        """

        if self.direction == 1:
            distance = entity.pos[0] - self.pos[0]
        else:
            distance = self.pos[0] - entity.pos[0]
        return (self.pos[1] - entity.pos[1] + entity.size[1] >= distance - entity.size[0]) \
            and (self.pos[1] - entity.pos[1] - entity.size[1] <= distance + entity.size[0])

    def disable_capacity(self):
        """
        Pyoro 2 doesn"t need this method so do nothing.
        """

    def remove(self):
        """
        Kill Pyoro 2 and remove its action delayed.
        """

        self.level.removeActionDelay((self, "update_shoot_sprite_id"))
        Pyoro.remove(self)
