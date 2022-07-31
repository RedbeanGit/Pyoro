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


def resize_image(image, new_size):
    """
    Resize a pygame surface by stretching its pixels.

    :type image: pygame.surface.Surface
    :param image: The surface to resize.

    :type new_size: (tuple)
    :param new_size: A (w, h) tuple where w and h are both integers.

    :rtype: pygame.surface.Surface
    :returns: A new pygame surface resized from the given one.
    """

    if len(new_size) != 2:
        return image
    new_size = (int(new_size[0]), int(new_size[1]))
    return pygame.transform.scale(image, new_size)


def invert_image(image, vertical, horizontal):
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


def stretch_image(image, new_size, border_size):
    """
    Try to stretch a pygame surface without deforming it. This technique is
            inspired by Android 9-patch. Only the center and borders of the image
            can stretch, leaving the corners and the thickness of the borders
            intact.

    :type image: pygame.surface.Surface
    :param image: The surface to resize.

    :type new_size: (tuple)
    :param new_size: A (w, h) tuple where w and h are both integers.

    :type border_size: int
    :param border_size: The thickness of the borders (kept after the
            operation).

    :rtype: pygame.surface.Surface
    :returns: A new pygame surface resized from the given one.
    """

    if len(new_size) != 2:
        return image

    new_size = (int(new_size[0]), int(new_size[1]))

    if border_size <= new_size[0] / 2 and border_size <= new_size[1] / 2:
        border_size = int(border_size)
    else:
        border_size = min(new_size) // 2

    if image.get_alpha is None:
        back = pygame.Surface(new_size).convert()
    else:
        back = pygame.Surface(new_size).convert_alpha()

    side_length = (
        image.get_size()[0] - border_size * 2,
        image.get_size()[1] - border_size * 2,
    )
    new_side_length = (new_size[0] - border_size * 2, new_size[1] - border_size * 2)

    back.blit(image.subsurface((0, 0), (border_size, border_size)).copy(), (0, 0))
    back.blit(
        pygame.transform.scale(
            image.subsurface((border_size, 0), (side_length[0], border_size)).copy(),
            (new_side_length[0], border_size),
        ),
        (border_size, 0),
    )
    back.blit(
        image.subsurface(
            (side_length[0] + border_size, 0), (border_size, border_size)
        ).copy(),
        (new_side_length[0] + border_size, 0),
    )
    back.blit(
        pygame.transform.scale(
            image.subsurface((0, border_size), (border_size, side_length[1])).copy(),
            (border_size, new_side_length[1]),
        ),
        (0, border_size),
    )
    back.blit(
        pygame.transform.scale(
            image.subsurface(
                (border_size, border_size), (side_length[0], side_length[1])
            ),
            (new_side_length[0], new_side_length[1]),
        ),
        (border_size, border_size),
    )
    back.blit(
        pygame.transform.scale(
            image.subsurface(
                (side_length[0] + border_size, border_size),
                (border_size, side_length[1]),
            ).copy(),
            (border_size, new_side_length[1]),
        ),
        (new_side_length[0] + border_size, border_size),
    )
    back.blit(
        image.subsurface(
            (0, side_length[1] + border_size), (border_size, border_size)
        ).copy(),
        (0, new_side_length[1] + border_size),
    )
    back.blit(
        pygame.transform.scale(
            image.subsurface(
                (border_size, side_length[1] + border_size),
                (side_length[0], border_size),
            ).copy(),
            (new_side_length[0], border_size),
        ),
        (border_size, new_side_length[1] + border_size),
    )
    back.blit(
        image.subsurface(
            (side_length[0] + border_size, side_length[1] + border_size),
            (border_size, border_size),
        ).copy(),
        (new_side_length[0] + border_size, new_side_length[1] + border_size),
    )
    return back
