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
Provide a class to draw a game.level.Level and entities.entity.Entity

Created on 11/10/2018
"""

import os
import pygame

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import CASE_SIZE, BACKGROUND_TRANSITION_DURATION, LEVEL_IMAGE_PATH
from game.level import Level
from game.util import get_monitor_density, get_screen_size
from gui.image_transformer import resize_image


class LevelDrawer:
    """
    Create a LevelDrawer object, usually used to draw a level and its
            entities on the screen.
    """

    def __init__(self, activity, game_id, bot_mode=False):
        """
        Initialize a new LevelDrawer object, create a new level and load
                background images.

        :type activity: gui.activity.Activity
        :param activity: The parent activity where to draw the level.

        :type game_id: int
        :param game_id: An integer representing Pyoro 1 or 2 (0=Pyoro,
                1=Pyoro 2).

        :type bot_mode: bool
        :param bot_mode: (Optional) Define if Pyoro have to be replaced by
                Pyobot. Default is False.
        """

        self.activity = activity
        self.images = {}
        self.case_size = ()
        self.level = None

        self.init_level(game_id, bot_mode)

        self.last_background_id = self.level.get_background_id_with_score()
        self.last_background = None

        self.init_images()

    def init_level(self, game_id, bot_mode):
        """
        Create a new level with given game_id and bot_mode value.

        :type game_id: int
        :param game_id: An integer representing Pyoro 1 or 2 (0=Pyoro,
                1=Pyoro 2).

        :type bot_mode: bool
        :param bot_mode: Define if Pyoro have to be replaced by Pyobot. Default
                is False.
        """

        self.level = Level(self, game_id, self.get_level_size(), bot_mode)

    def get_level_size(self):
        """
        Return the size of the level (the scale is expressed in case).

        :rtype: tuple
        :returns: A (w, h) tuple where w is an integer and h is a float
                number.
        """

        width_pixel, height_pixel = get_screen_size()
        horizontal_density, vertical_density = get_monitor_density()
        case_width, case_height = (
            horizontal_density * CASE_SIZE,
            vertical_density * CASE_SIZE,
        )
        return int(width_pixel / case_width), height_pixel / case_height

    def get_case_size(self):
        """
        Return the size of one case in pixel.


        :rtype: tuple
        :returns: A (w, h) tuple where w and h are both float numbers.
        """

        if not self.case_size:
            screen_width, screen_height = get_screen_size()
            if self.level:
                case_width, case_height = self.level.size
            else:
                case_width, case_height = self.get_level_size()
            self.case_size = screen_width / case_width, screen_height / case_height
        return self.case_size

    def init_images(self):
        """
        Initialize background images.
        """

        folder = os.path.join(LEVEL_IMAGE_PATH, "block")
        size = self.get_case_size()
        for i in range(3):
            image_name = f"block_{i}.png"
            self.images[image_name] = resize_image(
                self.activity.window.get_image(os.path.join(folder, image_name)), size
            )

        folder = os.path.join(LEVEL_IMAGE_PATH, f"background {self.level.game_id + 1}")
        size = self.activity.window.get_size()
        for i in range(21):
            image_name = f"background_{i}.png"
            self.images[image_name] = resize_image(
                self.activity.window.get_image(
                    os.path.join(folder, image_name), alpha_channel=False
                ),
                size,
            )

    def draw_pyoro(self):
        """
        Draw Pyoro (or Pyoro 2) and its tongue when he tries to catch a bean.
        """

        pyoro = self.level.pyoro
        tongue = pyoro.tongue
        case_size = self.get_case_size()
        if tongue:
            # define tongue colors (insideColor, outlineColor)
            style_type = self.level.get_style_type_with_score()
            if style_type == 0:
                color = ((255, 98, 183), (0, 0, 0))
            elif style_type == 1:
                color = ((178, 178, 178), (0, 0, 0))
            else:
                color = ((0, 0, 0), (255, 255, 255))

            # define tongue pos
            tx1 = tongue.pos[0] - tongue.size[0] * 0.5 * pyoro.direction
            tx2 = tongue.pos[0] - tongue.size[0] * 0.4 * pyoro.direction
            px1 = pyoro.pos[0] + pyoro.size[0] * 0.25 * pyoro.direction
            px2 = pyoro.pos[0] + pyoro.size[0] * 0.3125 * pyoro.direction

            ty1 = tongue.pos[1] + tongue.size[1] * 0.4
            ty2 = tongue.pos[1] + tongue.size[1] * 0.5
            py1 = pyoro.pos[1] - pyoro.size[1] * 0.125
            py2 = pyoro.pos[1] - pyoro.size[1] * 0.0625

            tongue_coords = [(px1, py1), (tx1, ty1), (tx2, ty2), (px2, py2)]

            for key, pos in enumerate(tongue_coords):
                x_pos = int(pos[0] * self.case_size[0] + 5)
                y_pos = int(pos[1] * self.case_size[1] + 5)
                tongue_coords[key] = (x_pos, y_pos)

            pygame.draw.polygon(
                self.activity.window.root_surface, color[0], tongue_coords
            )
            pygame.draw.line(
                self.activity.window.root_surface,
                color[1],
                tongue_coords[0],
                tongue_coords[1],
                int(0.115 * case_size[0]),
            )
            pygame.draw.line(
                self.activity.window.root_surface,
                color[1],
                tongue_coords[2],
                tongue_coords[3],
                int(3.68),
            )

        self.activity.window.draw_image(
            pyoro.images[pyoro.current_image_name],
            (
                (pyoro.pos[0] - pyoro.size[0] / 2) * case_size[0],
                (pyoro.pos[1] - pyoro.size[1] / 2) * case_size[1],
            ),
        )

    def draw_background(self):
        """
        Draw the appropriate background image by handling smooth transition
                animations between different background images.
        """

        back_id = self.level.get_background_id_with_score()
        background = self.images[f"background_{back_id}.png"]

        if back_id == 0:
            background.set_alpha(255)
        else:
            if self.last_background_id != back_id:
                self.last_background = self.images[
                    f"background_{self.last_background_id}.png"
                ]
                self.last_background_id = back_id

                self.last_background.set_alpha(255)
                background.set_alpha(0)

                self.update_background_transition(0)
            if background.get_alpha() != 255:
                self.activity.window.draw_image(self.last_background, (0, 0))
        self.activity.window.draw_image(background, (0, 0))

    def draw_blocks(self):
        """
        Draw the cases which are not destroyed.
        """

        _, height = self.activity.window.get_size()
        case_size = self.get_case_size()
        for i in range(self.level.size[0]):
            if self.level.cases[i].exists:
                self.activity.window.draw_image(
                    self.images[f"block_{self.level.get_style_type_with_score()}.png"],
                    (i * case_size[0], height - case_size[1]),
                )

    def update_background_transition(self, opacity):
        """
        Increase new background opacity to create a smooth transition
                animation.

        :type opacity: float
        :param opacity: Opacity of the new background image (1 <= opacity <= 255).
        """

        self.images[
            f"background_{self.level.get_background_id_with_score()}.png"
        ].set_alpha(opacity)

        if opacity < 255:
            self.level.set_action_delay(
                (self, "update_background_transition"),
                BACKGROUND_TRANSITION_DURATION / 128,
                self.update_background_transition,
                opacity + 2,
            )
        else:
            self.level.remove_action_delay((self, "update_background_transition"))

    def draw_entities(self):
        """
        Draw all entities stored in the level except Pyoro (There is another
                method to draw Pyoro).
        """

        width, height = self.get_case_size()
        for entity in self.level.entities:
            x_pos = (entity.pos[0] - entity.size[0] / 2) * width
            y_pos = (entity.pos[1] - entity.size[1] / 2) * height
            self.activity.window.draw_image(
                entity.images[entity.current_image_name], (x_pos, y_pos)
            )

    def update(self, delta_time):
        """
        Update the level drawer by drawing background, blocks, Pyoro and
                entities images.

        :type delta_time: float
        :param delta_time: Time elapsed since the last update.
        """

        self.level.update(delta_time)
        self.draw_background()
        self.draw_blocks()
        self.draw_pyoro()
        self.draw_entities()
