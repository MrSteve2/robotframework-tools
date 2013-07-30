# robotframework-tools
#
# Tools for Robot Framework and Test Libraries.
#
# Copyright (C) 2013 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# robotframework-tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# robotframework-tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with robotframework-tools. If not, see <http://www.gnu.org/licenses/>.

"""robotshell.magic

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['RobotMagics', 'RobotMagic', 'KeywordMagic', 'KeywordCellMagic']

from IPython.core.magic import Magics, magics_class, line_magic

@magics_class
class RobotMagics(Magics):
    def __init__(self, robot_plugin):
        Magics.__init__(self, robot_plugin.shell)

        self.robot_plugin = robot_plugin

    ## @line_magic
    ## def Robot(self, name=None):
    ##     return self.robot_plugin.Robot(name)

    @line_magic
    def Import(self, name):
        return self.robot_plugin.Import(name)

class RobotMagic(object):
    def __init__(self, robot_plugin, name=None):
        self.robot_plugin = robot_plugin
        self.name = name

    @property
    def __doc__(self):
        return self.robot.__doc__

    @property
    def robot(self):
        if self.name:
            return self.robot_plugin.robots[self.name]
        return self.robot_plugin.robot

    @property
    def magic_name(self):
        if self.name:
            return 'Robot.' + self.name
        return 'Robot'

    def __str__(self):
        return self.magic_name

    def __call__(self, magics, name):
        return self.robot_plugin.Robot(self.name or name)

class KeywordMagic(object):
    def __init__(self, keyword):
        self.keyword = keyword

    @property
    def __doc__(self):
        return self.keyword.__doc__

    def __str__(self):
        return self.keyword.name

    def __call__(self, magics, args_str):
        if not args_str:
            return self.keyword()

        if any(args_str.startswith(c) for c in '[|'):
            args = [s.strip() for s in args_str.strip('[|]').split('|')]
        else:
            args = args_str.split()
        return self.keyword.debug(*args)

class KeywordCellMagic(KeywordMagic):
    def __call__(self, magics, args_str):
        args = [s.strip() for s in args_str.strip().split('\n')]
        return self.keyword(*args)
