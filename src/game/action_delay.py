# -*- coding:utf-8 -*-

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
Provide a class to delay the call of a
function of method.

Created on 14/08/2018
"""

import time

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"


class ActionDelay:
    """
    Delay the call of a function or method of a defined time.
    """

    def __init__(self, wait_time, fct, *fct_args, **fct_kwargs):
        """
        Initialize an ActionDelay object.

        :type wait_time: float
        :param wait_time: Delay (in second).

        :type fct: function, method
        :param fct: The function or method to call.

        :type *fct_args: objects
        :param *fct_args: The arguments to pass to the function
                or method to run.

        :type **fct_kwargs: objects
        :param **fct_kwargs: The optional arguments to pass to
                the function or method to run.
        """

        self.wait_time = wait_time
        self.passed_time = 0
        self.fct = fct
        self.fct_args = fct_args
        self.fct_kwargs = fct_kwargs
        self.last_time = time.time()

    def update(self, delta_time):
        """
        Update the timer.

        :type delta_time: float
        :param delta_time: Time elapsed since the last update.
        """

        self.passed_time += delta_time
        if self.passed_time >= self.wait_time:
            self.fct(*self.fct_args, **self.fct_kwargs)
