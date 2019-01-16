# -*- coding: utf-8 -*-

"""
Provide activities used to manage the game view.

Created on 16/01/2019
"""

__author__ = "Julien Dubois"
__version__ = "2.0.0"

from lemapi.view import View
from lemapi.widget import Image_widget


class Splash_view(View):
    def __init__(self):
        super().__init__()
        self.add_widget("pyoro_icon", Image_widget, None)
