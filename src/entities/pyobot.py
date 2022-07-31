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
Provide a Pyobot class, a Pyoro bot.

Created on 11/04/2018.
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.bean import Bean
from entities.pyoro import Pyoro


class Pyobot(Pyoro):
    """
    Create a Pyobot used in the main menu. This Pyoro automatically move to
        catch falling beans.
    """

    def update(self, delta_time):
        """
        Pyobot search for the best position to eat the lowest bean and update
            its position.

        :type delta_time: float
        :param delta_time: Time elapsed since the last update.
        """

        if not self.tongue:
            pos = self.get_nearest_pos(*self.get_pos_to_eat())
            if pos > 0 and pos < self.level.size[0]:
                if self.pos[0] > pos:
                    self.enable_move_left()
                elif self.pos[0] < pos:
                    self.enable_move_right()
            else:
                self.disable_move()

            if int(pos) == int(self.pos[0]):
                self.look_bean()
                self.enable_capacity()
        Pyoro.update(self, delta_time)

    def get_pos_to_eat(self):
        """
        Find the 2 horizontal position that could allow Pyobot to eat the
            lowest bean.

        :rtype: tuple
        :returns: A (pos1, pos2) tuple where pos1 is the leftmost position and
            pos2 is the rightmost one.
        """

        lowest_bean = self.get_lowest_bean()
        if lowest_bean:
            return lowest_bean.pos[0] - (
                self.level.size[1] - lowest_bean.pos[1]
            ), lowest_bean.pos[0] + (self.level.size[1] - lowest_bean.pos[1])
        return -1, self.level.size[0]

    def look_bean(self):
        """
        Turn Pyobot to make him look at the bean he will catch.
        """

        lowest_bean = self.get_lowest_bean()
        if lowest_bean:
            if self.pos[0] > lowest_bean.pos[0]:
                self.enable_move_left()
            else:
                self.enable_move_right()
        self.disable_move()

    def get_nearest_pos(self, pos1, pos2):
        """
        Return the nearest horizontal position from Pyobot.

        :type pos1: float
        :param pos1: The first horizontal position.

        :type pos2: float
        :param pos2: The second horizontal position.

        :rtype: float
        :returns: The best position between pos1 and pos2.
        """

        pos = sorted([pos1, pos2], key=lambda x: abs(self.pos[0] - x))
        if pos[0] <= 0 or pos[0] >= self.level.size[0]:
            return pos[1]
        return pos[0]

    def remove(self):
        """
        Reset the level (this entity can't die).
        """

        self.level.reset()

    def get_lowest_bean(self):
        """
        Find the bean which has the smallest vertical coordinate.

        :rtype: entities.bean.Bean
        :returns: The lowest bean.
        """

        best_entity = None
        for entity in self.level.entities:
            if isinstance(entity, Bean):
                if best_entity is None:
                    best_entity = entity
                elif entity.pos[1] > best_entity.pos[1]:
                    best_entity = entity
        return best_entity
