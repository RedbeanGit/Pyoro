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
Provide an activity to manage the real game view.

Created on 10/04/2018
"""

import os

from pygame.locals import (
    KEYDOWN,
    KEYUP,
    JOYBUTTONDOWN,
    JOYBUTTONUP,
    JOYHATMOTION,
    JOYAXISMOTION,
)

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.util import Game

from gui.activity import Activity
from gui.game_over_menu import GameOverMenu
from gui.level_drawer import LevelDrawer
from gui.pause_menu import PauseMenu
from gui.text import Text


class LevelActivity(Activity):
    """
    Activity managing in-game graphical components.
    """

    def __init__(self, window, game_id=0):
        """
        Initialize a new LevelActivity object.

        :type window: gui.window.Window
        :param window: The parent game window.

        :type game_id: int
        :param game_id: (Optional) The id of the game to load. It can be 0 or 1.
            0 = Pyoro, 1 = Pyoro 2. Default is 0.
        """

        self.window = window
        self.level_drawer = LevelDrawer(self, game_id)

        self.last_level_style_type = 0
        self.last_level_score = 0

        self.joy_hat_states = []
        self.joy_axis_states = []

        Activity.__init__(self, window)
        self.init_joy_states()

    def init_sounds(self):
        """
        Load sounds and musics which will be used later by this activity.
        """

        self.__init_sounds__(
            (
                "music_0",
                "music_1",
                "music_2",
                "drums",
                "organ",
                "game_over",
                "speed_drums",
            ),
            os.path.join("data", "audio", "musics"),
            "music",
        )
        Game.audio_player.set_speed(1)
        self.sounds["music_0"].play(-1)

    def init_widgets(self):
        """
        Create widgets which will be used later by this activity ("score" and "high
        score" text).
        """

        spos = self.layout.get_widget_pos("score_text")
        ssize = self.layout.get_font_size("score_text")

        hpos = self.layout.get_widget_pos("high_score_text")
        hsize = self.layout.get_font_size("high_score_text")

        self.add_widget(
            "score_text", Text, spos, "Score: 0", font_size=ssize, anchor=(0, -1)
        )
        self.add_widget(
            "high_score_text",
            Text,
            hpos,
            f"Meilleur Score: {self.get_high_score()}",
            font_size=hsize,
            anchor=(0, -1),
        )

    def init_joy_states(self):
        """
        Initialize joystick hat and axis values.
        """

        best_joy_hats = max(
            self.window.joysticks, key=lambda x: x.get_numhats(), default=None
        )
        best_joy_axis = max(
            self.window.joysticks, key=lambda x: x.get_numaxes(), default=None
        )
        if best_joy_hats:
            for _ in range(best_joy_hats.get_numhats()):
                self.joy_hat_states.append(None)
        if best_joy_axis:
            for i in range(best_joy_axis.get_numaxes()):
                self.joy_axis_states.append(None)

    # score
    def get_high_score(self):
        """
        Return the highest score from options.

        :rtype: int
        :returns: The highest score for the current game_id.
        """

        return Game.options.get("high score", [0, 0])[self.level_drawer.level.game_id]

    def set_high_score(self, score):
        """
        Define a new high score for the current game_id.
        """

        if "high score" not in Game.options:
            Game.options["high score"] = [0, 0]
        Game.options["high score"][self.level_drawer.level.game_id] = score

    def update_score(self):
        """
        Update the score text widget with the current score.
        """

        self.widgets["score_text"].text = f"Score: {self.level_drawer.level.score}"
        if self.level_drawer.level.score > self.get_high_score():
            self.widgets[
                "high_score_text"
            ].text = f"High Score: {self.level_drawer.level.score}"

    def update_sounds(self, delta_time):
        """
        Start or stop musics according to the current score.
        """

        style_type = self.level_drawer.level.get_style_type_with_score()

        # Normal style
        if style_type == 0:
            if self.last_level_score != self.level_drawer.level.score:

                if (
                    self.last_level_score < 5000
                    and self.level_drawer.level.score >= 5000
                ):
                    print(
                        "[INFO] [LevelActivity.update_sounds] Drums added to the music"
                    )
                    self.sounds["drums"].play(-1)
                    self.sounds["drums"].set_pos(self.sounds["music_0"].pos)

                elif (
                    self.last_level_score < 10000
                    and self.level_drawer.level.score >= 10000
                ):
                    print(
                        "[INFO] [LevelActivity.update_sounds] Organ added to the music"
                    )
                    self.sounds["organ"].play(-1)
                    self.sounds["organ"].set_pos(self.sounds["music_0"].pos)

        # Black and white style
        elif style_type == 1:
            if self.last_level_style_type != style_type:
                print("[INFO] [LevelActivity.update_sounds] Music 2 started")
                Game.audio_player.set_speed(1)
                Game.audio_player.stop_audio()
                self.sounds["music_1"].play(-1)

        # Flashy style
        elif style_type == 2:
            if self.last_level_style_type != style_type:
                print("[INFO] [LevelActivity.update_sounds] Music 3 started")
                Game.audio_player.set_speed(1)
                Game.audio_player.stop_audio()
                self.sounds["music_2"].play(-1)

            if self.last_level_score < 41000 and self.level_drawer.level.score >= 41000:
                print(
                    "[INFO] [LevelActivity.update_sounds] Speed drums added to the music"
                )
                self.sounds["speed_drums"].play(-1)
                self.sounds["speed_drums"].set_pos(self.sounds["music_2"].pos)

        self.last_level_style_type = style_type
        self.last_level_score = self.level_drawer.level.score
        if not self.level_drawer.level.pyoro.dead:
            Game.audio_player.set_speed(
                Game.audio_player.get_speed() + 0.002 * delta_time
            )

    def save_level_state(self):
        """
        Save the score and the game_id of the current level.
        """

        if self.level_drawer.level.score > self.get_high_score():
            self.set_high_score(self.level_drawer.level.score)
        Game.options["last game"] = self.level_drawer.level.game_id

    def pause_game(self):
        """
        Stop updating the level.
        """

        if "pause_menu" in self.widgets:
            self.on_pause_menu_destroy()
        else:
            if "gameOverMenu" not in self.widgets:
                # Game.audio_player.pauseAudio()
                size = self.layout.get_widget_size("pause_menu")
                pos = self.layout.get_widget_pos("pause_menu")
                anchor = self.layout.get_widget_anchor("pause_menu")
                fsize = self.layout.get_font_size("pause_menu")

                self.add_widget(
                    "pause_menu",
                    PauseMenu,
                    pos,
                    self.on_pause_menu_destroy,
                    self.window.set_menu_render,
                    size=size,
                    anchor=anchor,
                    font_size=fsize,
                )
                self.level_drawer.level.loop_active = False

    def on_pause_menu_destroy(self):
        """
        This method is called when the pause menu is destroyed. It re-enable the
        level to be updated.
        """

        self.remove_widget("pause_menu")
        self.level_drawer.level.loop_active = True
        # Game.audio_player.unpauseAudio()

    def game_over(self):
        """
        Stop sounds and create a "game over" menu dialog.
        """

        Game.audio_player.stop_audio()
        Game.audio_player.set_speed(1)
        self.sounds["game_over"].play()

        size = self.layout.get_widget_size("game_over_menu")
        pos = self.layout.get_widget_pos("game_over_menu")
        anchor = self.layout.get_widget_anchor("game_over_menu")
        fsize = self.layout.get_font_size("game_over_menu")

        self.add_widget(
            "gameOverMenu",
            GameOverMenu,
            pos,
            self.level_drawer.level.score,
            self.on_game_over_menu_destroy,
            size=size,
            anchor=anchor,
            font_size=fsize,
        )

    def on_game_over_menu_destroy(self):
        """
        This method is called when the game over menu is destroyed. It makes the
        game return to the main menu.
        """

        self.remove_widget("gameOverMenu")
        self.window.set_menu_render()

    def update_event(self, event):
        """
        Update the level with
        """

        if self.level_drawer.level.loop_active:
            keyboard = Game.options.get("keyboard", {})
            joystick = Game.options.get("joystick", {})
            pyoro = self.level_drawer.level.pyoro

            enable_keys = {
                "left": pyoro.enable_move_left,
                "right": pyoro.enable_move_right,
                "action": pyoro.enable_capacity,
                "pause": self.pause_game,
            }
            disable_keys = {
                "left": pyoro.disable_move,
                "right": pyoro.disable_move,
                "action": pyoro.disable_capacity,
                "pause": lambda: None,
            }

            if event.type == KEYDOWN:
                for action_name, action in enable_keys.items():
                    if event.key == keyboard.get(action_name, None):
                        action()

            elif event.type == KEYUP:
                for action_name, action in disable_keys.items():
                    if event.key == keyboard.get(action_name, None):
                        action()

            elif event.type == JOYBUTTONDOWN:
                for action_name, input_infos in joystick.items():
                    if input_infos["inputType"] == JOYBUTTONDOWN:
                        if input_infos["buttonId"] == event.button:
                            enable_keys[action_name]()

            elif event.type == JOYBUTTONUP:
                for action_name, input_infos in joystick.items():
                    if input_infos["inputType"] == JOYBUTTONDOWN:
                        if input_infos["buttonId"] == event.button:
                            disable_keys[action_name]()

            elif event.type == JOYHATMOTION:
                enabled = event.value
                disabled = self.joy_hat_states[event.hat]
                self.joy_hat_states[event.hat] = enabled

                for action_name, input_infos in joystick.items():
                    if input_infos["inputType"] == JOYHATMOTION:
                        if input_infos["hatId"] == event.hat:
                            if input_infos["value"] == enabled:
                                enable_keys[action_name]()
                            elif input_infos["value"] == disabled:
                                disable_keys[action_name]()

            elif event.type == JOYAXISMOTION:
                enabled = event.value
                disabled = self.joy_axis_states[event.axis]
                self.joy_axis_states[event.axis] = enabled

                for action_name, input_infos in joystick.items():
                    if input_infos["inputType"] == JOYAXISMOTION:
                        if input_infos["axisId"] == event.axis:
                            if (
                                input_infos["value"] / enabled > 0
                                and abs(event.value) > 0.2
                            ):
                                enable_keys[action_name]()
                            elif disabled:
                                if (
                                    input_infos["value"] / disabled > 0
                                    or abs(event.value) <= 0.2
                                ):
                                    disable_keys[action_name]()

        Activity.update_event(self, event)

    def update(self, delta_time):
        """
        Update all graphical components of this activity.

        :type delta_time: float
        :param delta_time: Time elapsed since the last call of this method (in
            seconds).
        """

        self.level_drawer.update(delta_time)
        if self.level_drawer.level.loop_active:
            self.update_score()
            self.update_sounds(delta_time)
        Activity.update(self, delta_time)

    def destroy(self):
        """
        Destroy the activity and all its components.
        """

        self.save_level_state()
        Activity.destroy(self)
