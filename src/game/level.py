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
Provide a class to manage a game level (entities, flow of time,...)

Created on 18/03/2018
"""

import random

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from entities.angel import Angel
from entities.bean import Bean
from entities.leaf import Leaf
from entities.leaf_piece import LeafPiece
from entities.pink_bean import PinkBean
from entities.pyobot import Pyobot
from entities.pyobot_2 import Pyobot2
from entities.pyoro import Pyoro
from entities.pyoro_2 import Pyoro2
from entities.score_text import ScoreText
from entities.smoke import Smoke
from entities.super_bean import SuperBean

from game.config import BEAN_FREQUENCY, SPEED_ACCELERATION, \
    BACKGROUND_ANIMATED_DURATION
from game.util import Game


class Level:
    """
    Central class that manages the entities, terrain and more.
    """

    def __init__(self, level_drawer, game_id, size, bot_mode=False):
        """
        Initialize a new Level object.

        :type level_drawer: gui.level_drawer.Level_drawer
        :param activity: The graphical representation of this level.

        :type game_id: int
        :param game_id: It can be 0 for Pyoro, or 1 for Pyoro 2.

        :type size: tuple
        :param size: The size of the level (in blocks) in a (width, height)
            tuple where width and height are floating point values.

        :type bot_mode: bool
        :param bot_mode: Optional. If True, Pyoro will be a bot.
            Default is False.
        """

        self.level_drawer = level_drawer
        self.game_id = game_id
        self.size = size
        self.bot_mode = bot_mode

        self.loop_active = True
        self.pyoro = None

        self.score = 0
        self.speed = 1
        self.animated_background_id = 13

        self.cases = []
        self.entities = []
        self.action_delays = {}

        self.init_cases(self.size[0])
        self.init_pyoro()
        self.spawn_bean()

    def init_cases(self, nb_cases):
        """
        Create the terrain with new blocks.

        :type nb_cases: int
        :param nb_cases: The number of blocks which will compose the floor.
        """

        self.cases.clear()
        for i in range(nb_cases):
            self.cases.append(Case(i))

    def init_pyoro(self):
        """
        Create a new bird according to the current game_id
        and bot_mode.
        """

        if self.bot_mode and self.game_id:
            self.pyoro = Pyobot2(self)
        elif self.bot_mode:
            self.pyoro = Pyobot(self)
        elif self.game_id:
            self.pyoro = Pyoro2(self)
        else:
            self.pyoro = Pyoro(self)

    def reset(self):
        """
        Restart the level:
            - score = 0
            - speed = 1
            - entities are killed
            - action delayed are stopped
            - terrain is recreated
        """

        self.score = 0
        self.speed = 1
        for entity in self.entities:
            entity.remove()
        self.entities.clear()
        self.action_delays.clear()
        self.init_cases(self.size[0])
        self.spawn_bean()

    def update(self, delta_time):
        """
        Update the level, entities and action_delays.

        :type delta_time: float
        :param delta_time: Time elapsed since the last update.
        """

        if self.loop_active:
            self.speed += delta_time * SPEED_ACCELERATION
            self.pyoro.update(delta_time * self.speed)
            for entity in self.entities:
                entity.update(delta_time * self.speed)
            for action_delay in dict(self.action_delays).values():
                action_delay.update(delta_time * self.speed)

    def update_animated_background(self):
        """
        If the current background is animated, update it.
        """

        if self.animated_background_id < 20:
            self.animated_background_id = self.animated_background_id + 1
        else:
            self.animated_background_id = 13

    def spawn_bean(self):
        """
        Randomly spawn a new bean. Bean type is also random.
        """

        bean_type_id = random.randint(0, 5)
        pos = (random.randint(0, self.size[0] - 1) + 0.75, 0)
        speed = random.uniform(0.5, 1.5) * (self.speed ** 0.6)

        if bean_type_id < 4:
            bean = Bean(self, pos, speed)
        elif self.score < 5000 or bean_type_id == 4:
            bean = PinkBean(self, pos, speed)
        else:
            bean = SuperBean(self, pos, speed)

        self.entities.append(bean)
        self.set_action_delay((self, "spawn_bean"),
                              BEAN_FREQUENCY
                              * random.uniform(0.5, 1.5)
                              / (self.speed ** 1.5),
                              self.spawn_bean
                              )

    def spawn_angel(self, case):
        """
        Spawn a new angel only if case can be repaired.

        :type case: game.case.Case
        :param case: The block that will be repaired by the new angel.
        """

        if not case.exists and not case.isRepairing:
            self.entities.append(Angel(self, case))

    def spawn_score(self, score, pos):
        """
        Spawn a flashing text and increase the score.

        :type score: int
        :param score: The value to add to the current score.
            It can be 10, 50, 100, 300 or 1000.

        :type pos: Iterable<float>
        :param pos: The position of the flashing text.
        """

        allowed = (10, 50, 100, 300, 1000)
        if score in allowed:
            self.score += score
            self.entities.append(ScoreText(self, pos, score))
        else:
            print(f"[WARNING] [Level.addScore] {score} is an invalid "
                  + f"value ! Allowed are {allowed}")

    def spawn_smoke(self, pos):
        """
        Spawn smoke.

        :type pos: Iterable<float>
        :param pos: The position of the smoke.
        """
        self.entities.append(Smoke(self, pos))

    def spawn_leaf(self, pos, leaf_type):
        """
        Spawn leafs with random speed.

        :type pos: Iterable<float>
        :param pos: The position of the leaf.

        :type leaf_type: str
        :param leaf_type: The type of the leaf. It can be
            "", "pink" or "super".
        """

        speed = random.uniform(0.5, 1.5)
        self.entities.append(Leaf(self, pos, speed, leaf_type))

    def spawn_leaf_piece(self, pos, speed, leaf_piece_type, vel):
        """
        Spawn cut leaf.

        :type pos: Iterable<float>
        :param pos: The default position of the leaf.

        :type speed: float
        :param speed: The speed of the leaf.

        :type leaf_piece_type: str
        :param leaf_piece_type: The type of the leaf. It can be
            "", "pink" or "super".

        :type vel: float
        :param vel: The default horizontal velocity.
        """
        self.entities.append(LeafPiece(
            self, pos, speed, leaf_piece_type, vel))

    def repair_case(self, case=None):
        """
        Repair a block by spawning an angel.

        :type case: game.case.Case
        :param case: Optional. The block to repair. The leftmost destroyed
            block is chosen if undefined.
        """

        void_cases = self.get_void_cases()
        if void_cases:
            case = case if case in void_cases else random.choice(void_cases)
            self.spawn_angel(case)

    def create_action_delay(self, action_name, wait_time, fct, *fctArgs, **fctKwargs):
        """
        Create a new action_delay. See game.action_delay.Action_delay.
        If an action_delay already exists with the same name, do nothing.

        :type action_name: object
        :param action_name: The name given to the new action_delay.

        :type wait_time: float
        :param wait_time: The time to wait before calling fct.

        :type fct: function or method
        :param fct: The function or method to delay.

        :type *fctArgs: object
        :param *fctArgs: The arguments to pass to fct.

        :type **fctKwargs: object
        :param **fctKwargs: The optional arguments to pass to the fct.
        """

        if action_name not in self.action_delays:
            self.action_delays[action_name] = ActionDelay(
                wait_time, fct, *fctArgs, **fctKwargs)

    def set_action_delay(self, action_name, wait_time, fct, *fctArgs, **fctKwargs):
        """
        Create a new action_delay or replace an existing one.
        See game.action_delay.Action_delay.

        :type action_name: object
        :param action_name: The name given to the new action_delay.

        :type wait_time: float
        :param wait_time: The time to wait before calling fct.

        :type fct: function or method
        :param fct: The function or method to delay.

        :type *fctArgs: object
        :param *fctArgs: The arguments to pass to fct.

        :type **fctKwargs: object
        :param **fctKwargs: The optional arguments to pass to the fct.
        """

        self.action_delays[action_name] = ActionDelay(
            wait_time, fct, *fctArgs, **fctKwargs)

    def remove_action_delay(self, *action_names):
        """
        Remove action_delay(s).

        :type *action_names: str
        :param *action_names: The name of the action_delays to remove.
        """

        for action_name in action_names:
            self.action_delays.pop(action_name, None)

    def remove_entity(self, entity):
        """
        Remove an Entity.

        :type entity: entities.entity.Entity
        :param entity: The entity to remove.
        """

        if entity in self.entities:
            self.entities.remove(entity)
        else:
            print(
                f"[WARNING] [Level.remove_entity] Unable to remove {entity} from Entity list")

    def get_style_type_with_score(self, score=None):
        """
        Get the style id from the score.
        0 is normal, 1 is black and white and 2 is flashy.

        :type score: int
        :param score: Optional. A score. Use the current level score
            if undefined.

        :rtype: int
        :returns: The style id associated to the given score.
        """

        score = score if score else self.score
        if score < 20000:
            return 0
        elif score < 30000:
            return 1
        else:
            return 2

    def get_background_id_with_score(self, score=None):
        """
        Get the background id associated to a specified score.

        :type score: int
        :param score: Optional. A score. Use the current level score
            if undefined.

        :rtype: int
        :returns: The background id associated to the given score.
        """

        score = score if score else self.score
        if score < 11000:
            return score // 1000
        elif score < 20000:
            return 10
        elif score < 30000:
            return 11
        elif score < 40000:
            return 12
        else:
            self.create_action_delay((self, "updateAnimatedBackround"),
                                     BACKGROUND_ANIMATED_DURATION, self.update_animated_background)
            return self.animated_background_id

    def get_audio_player(self):
        """
        Get the current audio player.

        :rtype: audio.audio_player.Audio_player
        :returns: The audio player currently used by the game.
        """
        return Game.audioPlayer

    def get_void_cases(self):
        """
        Get the destroyed blocks that are not being repaired.

        :rtype: list<game.case.Case>
        :returns: A list of all destroyed blocks.
        """
        return [case for case in self.cases
                if not(case.exists) and not(case.isRepairing)]

    def set_size(self, size):
        """
        Define the level size (in case).

        :type size: tuple
        :param size: The size in blocks of the level.
        """

        self.size = tuple(size)
        self.init_cases(int(size[0]))
