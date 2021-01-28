# -*- coding:utf-8 -*-

#   This file is part of Pyoro (A Python fan game).
#
#   Metawars is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Metawars is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
Provide useful functions on pygame.surface.Surface.

Created on 18/08/2018.
"""

import pygame

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"


def resizeImage(image, newSize):
	"""
	Resize a pygame surface by stretching its pixels.

	:type image: pygame.surface.Surface
	:param image: The surface to resize.

	:type newSize: (tuple)
	:param newSize: A (w, h) tuple where w and h are both integers.

	:rtype: pygame.surface.Surface
	:returns: A new pygame surface resized from the given one.
	"""

	if len(newSize) != 2:
		return image
	newSize = (int(newSize[0]), int(newSize[1]))
	return pygame.transform.scale(image, newSize)


def invertImage(image, vertical, horizontal):
	"""
	Flip a pygame surface vertically and / or horizontally.

	:type image: pygame.surface.Surface
	:param image: The surface to flip.

	:type vertical: bool
	:param vertical: If True, flip the surface vertically.

	:type horizontal: bool
	:param horizontal: If True, flip the surface horizontally.	

	:rtype: pygame.surface.Surface
	:returns: A new pygame surface flipped from the given one.
	"""

	return pygame.transform.flip(image, vertical, horizontal)


def stretchImage(image, newSize, borderSize):
	"""
	Try to stretch a pygame surface without deforming it. This technique is
		inspired by Android 9-patch. Only the center and borders of the image
		can stretch, leaving the corners and the thickness of the borders
		intact.

	:type image: pygame.surface.Surface
	:param image: The surface to resize.

	:type newSize: (tuple)
	:param newSize: A (w, h) tuple where w and h are both integers.

	:type borderSize: int
	:param borderSize: The thickness of the borders (kept after the
		operation).

	:rtype: pygame.surface.Surface
	:returns: A new pygame surface resized from the given one.
	"""

	if len(newSize) != 2:
		return image

	newSize = (int(newSize[0]), int(newSize[1]))

	if borderSize <= newSize[0] / 2 and borderSize <= newSize[1] / 2:
		borderSize = int(borderSize)
	else:
		borderSize = min(newSize) // 2
	
	if image.get_alpha == None:
		back = pygame.Surface(newSize).convert()
	else:
		back = pygame.Surface(newSize).convert_alpha()

	sideLength = (image.get_size()[0] - borderSize * 2, image.get_size()[1] \
		- borderSize * 2)
	newSideLength = (newSize[0] - borderSize * 2, newSize[1] - borderSize * 2)

	back.blit(image.subsurface((0, 0), (borderSize, borderSize)).copy(), \
		(0, 0))
	back.blit(pygame.transform.scale(image.subsurface((borderSize, 0), \
		(sideLength[0], borderSize)).copy(), (newSideLength[0], \
		borderSize)), (borderSize, 0))
	back.blit(image.subsurface((sideLength[0] + borderSize, 0), (borderSize, \
		borderSize)).copy(), (newSideLength[0] + borderSize, 0))
	back.blit(pygame.transform.scale(image.subsurface((0, borderSize), \
		(borderSize, sideLength[1])).copy(), (borderSize, \
		newSideLength[1])), (0, borderSize))
	back.blit(pygame.transform.scale(image.subsurface((borderSize, \
		borderSize), (sideLength[0], sideLength[1])), (newSideLength[0], \
		newSideLength[1])), (borderSize, borderSize))
	back.blit(pygame.transform.scale(image.subsurface((sideLength[0] \
		+ borderSize, borderSize), (borderSize, sideLength[1])).copy(), \
		(borderSize, newSideLength[1])), (newSideLength[0] + borderSize, \
		borderSize))
	back.blit(image.subsurface((0, sideLength[1] + borderSize), (borderSize, \
		borderSize)).copy(), (0, newSideLength[1] + borderSize))
	back.blit(pygame.transform.scale(image.subsurface((borderSize, \
		sideLength[1] + borderSize), (sideLength[0], borderSize)).copy(), \
		(newSideLength[0], borderSize)), (borderSize, newSideLength[1] \
		+ borderSize))
	back.blit(image.subsurface((sideLength[0] + borderSize, sideLength[1] \
		+ borderSize), (borderSize, borderSize)).copy(), (newSideLength[0] \
		+ borderSize, newSideLength[1] + borderSize))
	return back
