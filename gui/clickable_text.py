# -*- coding: utf-8 -*-

"""
=========================
    @name: Pyoro
    @author: Ptijuju22
    @date: 10/04/2018
    @version: 1.1
=========================
"""

from gui.eventable_widget import Eventable_widget
from gui.text import Text

class Clickable_text(Text, Eventable_widget):
    """ Clickable text widget """

    DEFAULT_KWARGS = {
        "onClickTextColor": (200, 200, 200, 255),
        "onMiddleClickTextColor": (100, 100, 100, 255),
        "onRightClickTextColor": (220, 220, 220, 255),
        "onHoverTextColor": (230, 230, 230, 255),
        "disableTextColor": (240, 240, 240, 235)
    }

    def __init__(self, activity, pos, text, **kwargs):
        Clickable_text.updateDefaultKwargs(kwargs)
        Text.__init__(self, activity, pos, text, **kwargs)
        Eventable_widget.__init__(self, activity, pos, **self.kwargs)

    def update(self, deltaTime):
        if not self.kwargs["enable"]:
            self.font.fgcolor = self.kwargs["disableTextColor"]
        elif self.clicked:
            self.font.fgcolor = self.kwargs["onClickTextColor"]
        elif self.rightClicked:
            self.font.fgcolor = self.kwargs["onRightClickTextColor"]
        elif self.middleClicked:
            self.font.fgcolor = self.kwargs["onMiddleClickTextColor"]
        elif self.hovered:
            self.font.fgcolor = self.kwargs["onHoverTextColor"]
        else:
            self.font.fgcolor = self.kwargs["textColor"]
        Text.update(self, deltaTime)