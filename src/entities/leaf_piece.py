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
Provides a Leaf_piece class.
This entity is used as little leaf particles when a normal leaf is cut.

Created on 08/05/2018
"""

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import LEAF_SPRITE_DURATION
from entities.leaf import Leaf


class LeafPiece(Leaf):
    """
    Define a piece of leaf which appears when a normal leaf is cut. There are
        3 leaf types ("leaf", "pink leaf" and "super leaf") depending on the
        leaf that has just been cut.
    """

    def __init__(self, level, pos, speed, leafpieceType, vel=0):
        """
        Initialise a Leaf object.

        :type level: game.level.Level
        :param level: The level managing this entity.

        :type pos: list
        :param pos: The default position of the leaf in a [x, y] list where x
        and y are both float numbers.

        :type speed: float
        :param speed: The falling speed of the leaf.

        :type leafpieceType: str
        :param leafpieceType: The type of the leaf. It can be "leaf", "pink leaf"
        or "super leaf".

        :type vel: float
        :param vel: (Optional) The default velocity of the leaf.
        """

        Leaf.__init__(self, level, pos, speed, leafpieceType)
        self.vel = vel

    def init_images(self):
        """
        Load leaf_pieces images.
        """

        self.__init_images__(self.leaf_type)

    def update_sprite(self):
        """
        Update the images to create a flight animation.
        """

        score = self.level.get_style_type_with_score()

        self.sprite_index = self.sprite_index + 1 if self.sprite_index < 2 else 0
        self.current_image_name = f"leafpiece_{score}_{self.sprite_index}.png"

        self.level.set_action_delay((self, "update_sprite"),
                                    LEAF_SPRITE_DURATION, self.update_sprite)

    def cut(self):
        """
        A piece of leaf can't be cut so this method do nothing.
        """
