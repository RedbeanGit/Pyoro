# -*- coding: utf-8 -*-

"""
=========================
    @name: Pyoro
    @author: Ptijuju22
    @date: 29/03/2018
    @version: 1
=========================
"""

import os, pygame.freetype

from game.config import GUI_IMAGE_PATH
from gui.widget import Widget

class Text(Widget):

    DEFAULT_KWARGS = {
        "fontSize": 20,
        "font": os.path.join(GUI_IMAGE_PATH, "font.ttf"),
        
        "bold": False,
        "wide": False,
        "italic": False,
        "underline": False,
        "verticalMode": False,
        
        "textColor": (255, 255, 255, 255),
        "backgroundColor": None
    }

    def __init__(self, activity, pos, text, **kwargs):
        Text.updateDefaultKwargs(kwargs)
        Widget.__init__(self, activity, pos, **kwargs)
        self.text = text
        self.createFont()

    def createFont(self):
        self.font = pygame.freetype.Font(self.kwargs["font"])
        kwargs = dict(self.kwargs)
        kwargs.pop("font")
        self.config(**kwargs)

    def update(self, deltaTime):
        surface, rect = self.font.render(self.text, bgcolor = self.kwargs["backgroundColor"])
        self.kwargs["size"] = [rect.width, rect.height]
        self.activity.window.drawImage(surface, self.getRealPos())
        Widget.update(self, deltaTime)

    def config(self, **kwargs):
        Widget.config(self, **kwargs)
        if "font" in  kwargs:
            self.createFont()
        else:
            if "fontSize" in kwargs:
                self.font.size = kwargs["fontSize"]
            if "bold" in kwargs:
                self.font.strong = kwargs["bold"]
            if "wide" in kwargs:
                self.font.wide = kwargs["wide"]
            if "italic" in kwargs:
                self.font.oblique = kwargs["italic"]
            if "underline" in kwargs:
                self.font.underline = kwargs["underline"]
            if "verticalMode" in kwargs:
                self.font.vertical = kwargs["verticalMode"]
            if "textColor" in kwargs:
                self.font.fgcolor = kwargs["textColor"]