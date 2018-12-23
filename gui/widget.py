# -*- coding: utf-8 -*-

"""
=========================
    @name: Pyoro
    @author: Ptijuju22
    @date: 28/03/2018
    @version: 1.1
=========================
"""

from game.config import WIDTH, HEIGHT

class Widget:

    DEFAULT_KWARGS = {
        "size": [WIDTH, HEIGHT],
        "anchor": (-1, -1)
    }

    def __init__(self, activity, pos, **kwargs):
        Widget.updateDefaultKwargs(kwargs)
        self.activity = activity
        self.pos = pos
        self.isDestroyed = False
        self.kwargs = dict(kwargs)

    @classmethod
    def updateDefaultKwargs(cls, kwargs):
        for key, value in cls.DEFAULT_KWARGS.items():
            if key not in kwargs:
                kwargs[key] = value

    def update(self, deltaTime):
        pass
    
    def onEvent(self, event):
        pass

    def config(self, **kwargs):
        for key, value in kwargs.items():
            self.kwargs[key] = value
            
    def getRealPos(self):
        return [int(self.pos[0] - self.kwargs["size"][0] * (self.kwargs["anchor"][0] + 1) / 2), \
        int(self.pos[1] - self.kwargs["size"][1] * (self.kwargs["anchor"][1] + 1) / 2)]
    
    def isInWidget(self, pos):
        realPos = self.getRealPos()
        return pos[0] >= realPos[0] \
           and pos[0] <= realPos[0] + self.kwargs["size"][0] \
           and pos[1] >= realPos[1] \
           and pos[1] <= realPos[1] + self.kwargs["size"][1]

    def destroy(self):
        self.isDestroyed = True