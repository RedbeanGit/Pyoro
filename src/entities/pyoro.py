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

from entities.entity import Entity
from entities.tongue import Tongue
from game.config import PYORO_SPEED, PYORO_NOTCH_DURATION,  \
    PYORO_EATING_DURATION, PYORO_DIE_SPEED


class Pyoro(Entity):
    """
    Create a Pyoro (a little red bird) controlled by the player in game.
    """

    def __init__(self, level):
        """
        Initialize a new Pyoro object.

        :type level: game.level.Level
        :param level: The level managing this entity.
        """

        self.moving = False
        self.notch = False
        self.dead = False
        self.tongue = None
        self.eating_count = 0
        self.direction = 1
        _, height = level.size
        Entity.__init__(self, level, (2, height - 2), (2, 2))

    def init_images(self):
        """
        Initialize Pyoro images.
        """

        self.__init_images__("pyoro 1")

    def init_sounds(self):
        """
        Load Pyoro sounds.
        """

        self.__init_sounds__(("pyoro_move", "pyoro_die"))

    # directions
    def enable_move_right(self):
        """
        Make Pyoro move to the right by defining its direction.
        """

        if not self.dead and not self.tongue:
            self.direction = 1
            self.moving = True
            self.sounds["pyoro_move"].play(-1)

    def enable_move_left(self):
        """
        Make Pyoro move to the left by defining its direction.
        """

        if not self.dead and not self.tongue:
            self.direction = -1
            self.moving = True
            self.sounds["pyoro_move"].play(-1)

    def disable_move(self):
        """
        Stop Pyoro movement.
        """

        if self.sounds["pyoro_move"].isPlaying:
            self.sounds["pyoro_move"].pause()
        self.moving = False
        self.notch = False

    def move(self, delta_time):
        """
        Update Pyoro's position according to elapsed time.

        :type delta_time: float
        :param delta_time: Time elapsed since the last update.
        """

        if not self.dead and not self.tongue:
            if not self.notch:
                if self.direction == 1:
                    new_pos = self.pos[0] + self.size[0] / 2 + PYORO_SPEED \
                        * delta_time
                    void_pos = self.get_void_case_pos_on_path(new_pos)

                    if new_pos >= self.level.size[0]:
                        self.pos[0] = self.level.size[0] - self.size[0] / 2
                    elif void_pos is not None:
                        self.pos[0] = void_pos - self.size[0] / 2
                    else:
                        self.pos[0] += PYORO_SPEED * delta_time

                else:
                    new_pos = self.pos[0] - self.size[0] / 2 - PYORO_SPEED \
                        * delta_time
                    void_pos = self.get_void_case_pos_on_path(new_pos)
                    if new_pos < 0:
                        self.pos[0] = self.size[0] / 2
                    elif void_pos is not None:
                        self.pos[0] = void_pos + self.size[0] / 2 + 1
                    else:
                        self.pos[0] -= PYORO_SPEED * delta_time
                self.level.createActionDelay((self, "enable_notch"),
                                             PYORO_NOTCH_DURATION, self.enable_notch)

    def get_void_case_pos_on_path(self, new_pos):
        """
        Find the nearest hole from Pyoro. If there is no hole, return None.

        :type new_pos: float
        :param new_pos: The horizontal position where Pyoro try to go.

        :rtype: int, None
        :returns: The nearest destroyed case index (or none if there is no
            destroyed case).
        """

        if self.pos[0] < new_pos:
            old_pos = int(self.pos[0] + self.size[0] / 2)
            new_pos = min(int(new_pos), len(self.level.cases) - 1)
            for i in range(old_pos, new_pos + 1):
                if not self.level.cases[i].exists:
                    return i
        else:
            old_pos = int(self.pos[0] - self.size[0] / 2 - 1)
            new_pos = max(int(new_pos), 0)
            for i in range(old_pos, new_pos - 1, -1):
                if not self.level.cases[i].exists:
                    return i
        return None

    def enable_notch(self):
        """
        Make Pyoro do a little jump.
        """

        self.notch = True
        self.level.removeActionDelay((self, "enable_notch"))
        self.level.createActionDelay((self, "disable_notch"),
                                     PYORO_NOTCH_DURATION, self.disable_notch)

    def disable_notch(self):
        """
        Make Pyoro return to normal posture.
        """

        self.notch = False
        self.level.removeActionDelay((self, "disable_notch"))

    # update method
    def update(self, delta_time):
        """
        Update Pyoro (position, posture and sprite).

        :type delta_time: float
        :param delta_time: Time elapsed since the last update.
        """

        if self.moving:
            self.move(delta_time)
        else:
            self.level.removeActionDelay((self, "enable_notch"))
            self.disable_notch()
        self.update_sprite()

        if self.dead:
            if self.pos[1] - self.size[1] / 2 < self.level.size[0]:
                self.pos[1] += PYORO_DIE_SPEED * delta_time

    def update_sprite(self):
        """
        Define the sprite to use (normal, eating, jumping, catching, dying)
        """

        if self.eating_count:
            self.level.createActionDelay((self, "update_eating_count"),
                                         PYORO_EATING_DURATION, self.update_eating_count)

        style_type = self.level.get_style_type_with_score()
        if self.dead:
            image_name = "pyoro_{}_die_{}.png"
        elif self.tongue:
            image_name = "pyoro_{}_eat_1_{}.png"
        elif self.notch:
            image_name = "pyoro_{}_jump_{}.png"
        elif self.eating_count % 2:
            image_name = "pyoro_{}_eat_0_{}.png"
        else:
            image_name = "pyoro_{}_normal_{}.png"

        self.current_image_name = image_name.format(style_type, self.direction)

    def update_eating_count(self):
        """
        Update eating count value while in eating animation.
        """

        self.eating_count += 1
        if self.eating_count < 8:
            self.level.setActionDelay((self, "update_eating_count"),
                                      PYORO_EATING_DURATION, self.update_eating_count)
        else:
            self.eating_count = 0
            self.level.removeActionDelay((self, "update_eating_count"))

    def enable_capacity(self):
        """
        Stop Pyoro and make him sticks out his tongue.
        """

        if not self.dead:
            self.sounds["pyoro_move"].pause()
            if self.tongue:
                self.tongue.remove()
            self.tongue = Tongue(self.level, self.direction)
            self.level.entities.append(self.tongue)

    def disable_capacity(self):
        """
        Stop Pyoro from sticking out his tongue.
        """

        if not self.dead:
            if self.tongue:
                self.tongue.goBack = True

    def remove(self):
        """
        Remove Pyoro's tongue and kill him starting its death animation.
        """

        if not self.dead:
            self.dead = True
            if self.tongue:
                self.tongue.remove()

            self.disable_move()

            self.level.removeActionDelay((self, "enable_notch"),
                                         (self, "disable_notch"), (self, "update_eating_count"))

            self.level.createActionDelay((self, "gameOver"), 1.28,
                                         self.level.levelDrawer.activity.gameOver)
            self.level.createActionDelay((self, "removeGameOverActionDelay"),
                                         1.29, self.level.removeActionDelay, (self, "gameOver"))

            self.level.getAudioPlayer().speed = 1
            self.sounds["pyoro_die"].play()
