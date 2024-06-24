import os
import pyglet

from pyoro.banks.bank import Bank
from pyoro.events.event import Event
from pyoro.events.event_dispatcher import EventDispatcher
from pyoro.events.event_kind import EventKind

IMAGE_IDS = {
    # Angels
    "angel_normal": "res/images/angels/angel_normal.png",
    "angel_fly": "res/images/angels/angel_fly.png",
    # Backgrounds 1
    "background_1_1": "res/images/backgrounds_1/background_1_1.png",
    "background_1_2": "res/images/backgrounds_1/background_1_2.png",
    "background_1_3": "res/images/backgrounds_1/background_1_3.png",
    "background_1_4": "res/images/backgrounds_1/background_1_4.png",
    "background_1_5": "res/images/backgrounds_1/background_1_5.png",
    "background_1_6": "res/images/backgrounds_1/background_1_6.png",
    "background_1_7": "res/images/backgrounds_1/background_1_7.png",
    "background_1_8": "res/images/backgrounds_1/background_1_8.png",
    "background_1_9": "res/images/backgrounds_1/background_1_9.png",
    "background_1_10": "res/images/backgrounds_1/background_1_10.png",
    "background_1_11": "res/images/backgrounds_1/background_1_11.png",
    "background_1_12": "res/images/backgrounds_1/background_1_12.png",
    "background_1_13": "res/images/backgrounds_1/background_1_13.png",
    "background_1_14": "res/images/backgrounds_1/background_1_14.png",
    "background_1_15": "res/images/backgrounds_1/background_1_15.png",
    "background_1_16": "res/images/backgrounds_1/background_1_16.png",
    "background_1_17": "res/images/backgrounds_1/background_1_17.png",
    "background_1_18": "res/images/backgrounds_1/background_1_18.png",
    "background_1_19": "res/images/backgrounds_1/background_1_19.png",
    "background_1_20": "res/images/backgrounds_1/background_1_20.png",
    # Backgrounds 2
    "background_2_1": "res/images/backgrounds_2/background_2_1.png",
    "background_2_2": "res/images/backgrounds_2/background_2_2.png",
    "background_2_3": "res/images/backgrounds_2/background_2_3.png",
    "background_2_4": "res/images/backgrounds_2/background_2_4.png",
    "background_2_5": "res/images/backgrounds_2/background_2_5.png",
    "background_2_6": "res/images/backgrounds_2/background_2_6.png",
    "background_2_7": "res/images/backgrounds_2/background_2_7.png",
    "background_2_8": "res/images/backgrounds_2/background_2_8.png",
    "background_2_9": "res/images/backgrounds_2/background_2_9.png",
    "background_2_10": "res/images/backgrounds_2/background_2_10.png",
    "background_2_11": "res/images/backgrounds_2/background_2_11.png",
    "background_2_12": "res/images/backgrounds_2/background_2_12.png",
    "background_2_13": "res/images/backgrounds_2/background_2_13.png",
    "background_2_14": "res/images/backgrounds_2/background_2_14.png",
    "background_2_15": "res/images/backgrounds_2/background_2_15.png",
    "background_2_16": "res/images/backgrounds_2/background_2_16.png",
    "background_2_17": "res/images/backgrounds_2/background_2_17.png",
    "background_2_18": "res/images/backgrounds_2/background_2_18.png",
    "background_2_19": "res/images/backgrounds_2/background_2_19.png",
    "background_2_20": "res/images/backgrounds_2/background_2_20.png",
    # Green Beans
    "bean_green_left": "res/images/beans_green/bean_green_left.png",
    "bean_green_middle": "res/images/beans_green/bean_green_middle.png",
    "bean_green_right": "res/images/beans_green/bean_green_right.png",
    # GUI
    "gui_title": "res/images/gui/title.png",
    # Pink Beans
    "bean_pink_left": "res/images/beans_pink/bean_pink_left.png",
    "bean_pink_middle": "res/images/beans_pink/bean_pink_middle.png",
    "bean_pink_right": "res/images/beans_pink/bean_pink_right.png",
    # Cases
    "case": "res/images/cases/case.png",
    # Explosions
    "explosion_0": "res/images/explosions/explosion_0.png",
    "explosion_1": "res/images/explosions/explosion_1.png",
    "explosion_2": "res/images/explosions/explosion_2.png",
    # Pyoro
    "pyoro_normal": "res/images/pyoros/pyoro_normal.png",
    "pyoro_dead": "res/images/pyoros/pyoro_dead.png",
    "pyoro_tongue": "res/images/pyoros/pyoro_tongue.png",
    "pyoro_eat": "res/images/pyoros/pyoro_eat.png",
    "pyoro_jump": "res/images/pyoros/pyoro_jump.png",
    # Pyoro 2
    "pyoro_2_normal": "res/images/pyoros_2/pyoro_2_normal.png",
    "pyoro_2_dead": "res/images/pyoros_2/pyoro_2_dead.png",
    "pyoro_2_shoot_1": "res/images/pyoros_2/pyoro_2_shoot_1.png",
    "pyoro_2_shoot_2": "res/images/pyoros_2/pyoro_2_shoot_2.png",
    "pyoro_2_shoot_3": "res/images/pyoros_2/pyoro_2_shoot_3.png",
    "pyoro_2_shoot_4": "res/images/pyoros_2/pyoro_2_shoot_4.png",
    "pyoro_2_jump": "res/images/pyoros_2/pyoro_2_jump.png",
    # Scores
    "score_10": "res/images/scores/score_10.png",
    "score_50": "res/images/scores/score_50.png",
    "score_100": "res/images/scores/score_100.png",
    "score_300_0": "res/images/scores/score_300_0.png",
    "score_300_1": "res/images/scores/score_300_1.png",
    "score_300_2": "res/images/scores/score_300_2.png",
    "score_300_3": "res/images/scores/score_300_3.png",
    "score_300_4": "res/images/scores/score_300_4.png",
    "score_300_5": "res/images/scores/score_300_5.png",
    "score_1000_0": "res/images/scores/score_1000_0.png",
    "score_1000_1": "res/images/scores/score_1000_1.png",
    "score_1000_2": "res/images/scores/score_1000_2.png",
    "score_1000_3": "res/images/scores/score_1000_3.png",
    "score_1000_4": "res/images/scores/score_1000_4.png",
    "score_1000_5": "res/images/scores/score_1000_5.png",
    # Tongue
    "tongue": "res/images/tongues/tongue.png",
    "tongue_piece": "res/images/tongues/tongue_piece.png",
}


class ImageBank(
    Bank["pyglet.image.ImageData"]
):  # Use forward ref to prevent ImagePattern not found error
    def load(self):
        for key, value in IMAGE_IDS.items():
            if os.path.exists(value):
                self.data[key] = pyglet.image.load(value)  # type: ignore
        event_dispatcher = EventDispatcher.get_instance()
        event_dispatcher.push(Event(EventKind.ASSETS_LOADED, {"bank": "image"}))
