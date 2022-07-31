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
Provide a Seed class for Pyoro 2 shoot animation.

Created on 27/03/2018.
"""

import math
import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.entity import Entity
from gui.image_transformer import resize_image
from game.config import SEED_SPEED, AIR_RESISTANCE, GRAVITY_FORCE, ENTITIES_IMAGE_PATH


class Seed(Entity):
    """
    Create seeds used for Pyoro 2 shoot animations.
    """

    def __init__(self, level, angle, direction):
        """
        Initialize a new Seed object.

        :type level: game.level.Level
        :param level: The level managing this object

        :type angle: float
        :param angle: The initial trajectory's angle in degree.

        :type direction: int
        :param direction: The direction of the seed (1=right, -1=left).
        """

        self.direction = direction
        self.sprite_alpha = 255
        self.vel = [
            math.cos(angle * math.pi / 180) * direction * SEED_SPEED,
            -math.sin(angle * math.pi / 180) * SEED_SPEED,
        ]

        pos = (
            level.pyoro.pos[0] + (level.pyoro.size[0] / 2 + 0.0625) * direction,
            level.pyoro.pos[1] - level.pyoro.size[1] / 2 + 0.0625,
        )

        Entity.__init__(self, level, pos, (0.125, 0.125))

    def __init_images__(self, folder_name):
        """
        Internally load seed images in memory.

        :type folder_name: str
        :param folder_name: The path to the folder containing the seeds.
        """

        self.images = {}
        folder = os.path.join(ENTITIES_IMAGE_PATH, folder_name)
        image_names = os.listdir(folder)
        case_size = self.level.level_drawer.get_case_size()

        for image_name in image_names:
            if image_name.split(".")[-1] == "png":
                self.images[image_name] = resize_image(
                    self.level.level_drawer.activity.window.get_image(
                        os.path.join(folder, image_name), alpha_channel=False
                    ),
                    (case_size[0] * self.size[0], case_size[1] * self.size[1]),
                )
                self.images[image_name].set_alpha(self.sprite_alpha)
                self.current_image_name = image_name

    def init_images(self):
        """
        Initialize seed images.
        """

        self.__init_images__("seed")

    def update(self, deltaTime):
        """
        Update the seed (velocity, position, image opacity).

        :type deltaTime: float
        :param deltaTime: Time elapsed since the last update.
        """

        self.vel[0] -= AIR_RESISTANCE * self.direction * deltaTime
        self.vel[1] += GRAVITY_FORCE * deltaTime
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        if self.sprite_alpha > 0:
            self.sprite_alpha -= 64 * deltaTime
        else:
            self.remove()
        Entity.update(self, deltaTime)

    def update_sprite(self):
        """
        Define the sprite to use according to the current level style
        """

        self.current_image_name = f"seed_{self.level.get_style_type_with_score()}.png"
        self.images[self.current_image_name].set_alpha(self.sprite_alpha)
