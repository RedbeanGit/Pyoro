# -*- coding: utf-8 -*-

"""
Provide activities used to manage the game view.

Created on 16/01/2019
"""

from game.config import ENTITIES_IMAGE_PATH, WINDOW_COLOR, GUI_IMAGE_PATH
from graphism.widget import Play_button, Option_menu, Pause_menu, Game_over_menu, Normal_button

__author__ = "Julien Dubois"
__version__ = "2.0.0"

import os
from lemapi.api import get_gui
from lemapi.view import View
from lemapi.widget import Image_widget, Text


class Splash_view(View):
    def __init__(self):
        super().__init__()

    def init_widgets(self):
        gui = get_gui()
        w, h = gui.get_size()
        path = os.path.join(ENTITIES_IMAGE_PATH, "pyoro 1", \
            "pyoro_0_normal_1.png")
        gui.load_image(path)

        self.add_widget("pyoro_icon", Image_widget, (w * 0.5, h * 0.45), path, \
            anchor=(0, 0), size=(h * 0.25, h * 0.25))
        self.add_widget("info_text", Text, (w * 0.5, h * 0.75), "Chargement...", \
            anchor=(0, 0), fontSize=20)

    def update(self):
        gui = get_gui()
        w, h = gui.get_size()
        gui.draw_color(WINDOW_COLOR, (0, 0), (w, h))
        super().update()


class Menu_view(View):
    def __init__(self):
        super().__init__()

    def init_widgets(self):
        gui = get_gui()
        w, h = gui.get_size()
        path = os.path.join(GUI_IMAGE_PATH, "title.png")

        self.add_widget("title_image", Image_widget, (w * 0.5, h * 0.05), path, \
            anchor=(0, -1), size=(w * 0.4, h * 0.22))
        self.add_widget("play_button", Play_button, (w * 0.3, h * 0.55), 0, \
            anchor=(0, 0), size=(h * 0.3, h * 0.3))
        self.add_widget("play_button_2", Play_button, (w * 0.7, h * 0.55), 1, \
            anchor=(0, 0), size=(h * 0.3, h * 0.3))
        self.add_widget("option_button", Normal_button, (w * 0.3, h * 0.8), \
            anchor=(0, 0), size=(h * 0.3, h * 0.1), text="Options")
        self.add_widget("quit_button", Normal_button, (w * 0.7, h * 0.8), \
            anchor=(0, 0), size=(h * 0.3, h * 0.1), text="Quitter")

    def createOptionMenu(self, destroyFct, soundFct, soundVolumes):
        w, h = get_gui().get_size()
        self.add_widget("option_menu", Option_menu, (w * 0.5, h * 0.5), \
            destroyFct, soundFct, soundVolumes, anchor=(0, 0), size=(w * 0.8, h * 0.8))


class Level_view(View):
    def __init__(self):
        super().__init__()

    def init_widgets(self):
        gui = get_gui()
        w, h = gui.get_size()
        self.add_widget("score_text", Text, (w * 0.25, h * 0.05), "Score : 0", \
            anchor=(0, -1), fontSize=18)
        self.add_widget("high_score_text", Text, (w * 0.75, h * 0.05), \
            "Meilleur score : 0", anchor=(0, -1), fontSize=18)

    def createOptionMenu(self, destroyFct, soundFct, soundVolumes):
        w, h = get_gui().get_size()
        self.add_widget("option_menu", Option_menu, (w * 0.5, h * 0.5), \
            destroyFct, soundFct, soundVolumes, anchor=(0, 0), \
            size=(w * 0.8, h * 0.8))

    def createPauseMenu(self, destroyFct, quitFct, optionFct):
        w, h = get_gui().get_size()
        self.add_widget("pause_menu", Pause_menu, (w * 0.5, h * 0.5), \
            destroyFct, quitFct, optionFct, anchor=(0, 0), \
            size=(w * 0.25, h * 0.4))

    def createGameOverMenu(self, quitFct, score):
        w, h = get_gui().get_size()
        self.add_widget("option_menu", Game_over_menu, (w * 0.5, h * 0.5), \
            quitFct, score, anchor=(0, 0), size=(w * 0.25, h * 0.4))
