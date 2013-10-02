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

"""robotshell

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['Extension', 'load_robotshell']

from .plugin import RobotPlugin

from .robot import Extension

robot_plugin = None

def load_ipython_extension(shell):
    global robot_plugin
    if robot_plugin:
        return
    robot_plugin = RobotPlugin(shell=shell)
    try:
        shell.plugin_manager.register_plugin('robot', robot_plugin)
    except AttributeError:
        pass

def load_robotshell(shell, extensions=[]):
    load_ipython_extension(shell)
    for extcls in extensions:
        robot_plugin.register_extension(extcls)
