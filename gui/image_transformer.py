# -*- coding:utf-8 -*-

"""
=========================
    @name: Pyoro
    @author: Ptijuju22
    @date: 18/08/2018
    @version: 1.1
=========================
"""

import pygame

class Image_transformer:
    @staticmethod
    def resize(image, newSize):
        if len(newSize) != 2:
            return image
        newSize = (int(newSize[0]), int(newSize[1]))
        return pygame.transform.scale(image, newSize)

    @staticmethod
    def invert(image, vertical, horizontal):
        return pygame.transform.flip(image, vertical, horizontal)
        
    @staticmethod
    def stretch(image, newSize, borderSize):
        if len(newSize) != 2:
            return image
        newSize = (int(newSize[0]), int(newSize[1]))
        borderSize = int(borderSize) if borderSize <= newSize[0] / 2 and borderSize <= newSize[1] / 2 else min(newSize) // 2
        if image.get_alpha == None:
            back = pygame.Surface(newSize).convert()
        else:
            back = pygame.Surface(newSize).convert_alpha()

        sideLength = (image.get_size()[0] - borderSize * 2, image.get_size()[1] - borderSize * 2)
        newSideLength = (newSize[0] - borderSize * 2, newSize[1] - borderSize * 2)
        
        back.blit(image.subsurface((0, 0), (borderSize, borderSize)).copy(), (0, 0))
        back.blit(pygame.transform.scale(image.subsurface((borderSize, 0), (sideLength[0], borderSize)).copy(), (newSideLength[0], borderSize)), (borderSize, 0))
        back.blit(image.subsurface((sideLength[0] + borderSize, 0), (borderSize, borderSize)).copy(), (newSideLength[0] + borderSize, 0))
        back.blit(pygame.transform.scale(image.subsurface((0, borderSize), (borderSize, sideLength[1])).copy(), (borderSize,  newSideLength[1])), (0, borderSize))
        back.blit(pygame.transform.scale(image.subsurface((borderSize, borderSize), (sideLength[0], sideLength[1])), (newSideLength[0], newSideLength[1])), (borderSize, borderSize))
        back.blit(pygame.transform.scale(image.subsurface((sideLength[0] + borderSize, borderSize), (borderSize, sideLength[1])).copy(), (borderSize, newSideLength[1])), (newSideLength[0] + borderSize, borderSize))
        back.blit(image.subsurface((0, sideLength[1] + borderSize), (borderSize, borderSize)).copy(), (0, newSideLength[1] + borderSize))
        back.blit(pygame.transform.scale(image.subsurface((borderSize, sideLength[1] + borderSize), (sideLength[0], borderSize)).copy(), (newSideLength[0], borderSize)), (borderSize, newSideLength[1] + borderSize))
        back.blit(image.subsurface((sideLength[0] + borderSize, sideLength[1] + borderSize), (borderSize, borderSize)).copy(), (newSideLength[0] + borderSize, newSideLength[1] + borderSize))
        return back