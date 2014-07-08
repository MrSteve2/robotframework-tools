# robotframework-tools
#
# Python Tools for Robot Framework and Test Libraries.
#
# Copyright (C) 2013-2014 Stefan Zimmermann <zimmermann.code@gmail.com>
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

"""robottools.remote

- Provides the RemoteRobot, combining TestRobot with RobotRemoteServer.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['RemoteRobot']

from itertools import chain

from robotremoteserver import RobotRemoteServer

import robottools
from robottools import TestRobot, testlibrary
from robottools.testrobot import Keyword

from robottools import __version__, __requires__
__requires__ += robottools.__extras__['remote']


class RemoteLibrary(object):
    def __init__(self, robot):
        self.robot = robot

    def get_keyword_names(self):
        return list(chain(*map(dir, self.robot._libraries.values())))

    def get_keyword_arguments(self, name):
        keyword = self.robot[name]
        return list(keyword.arguments)

    def get_keyword_documentation(self, name):
        keyword = self.robot[name]
        return keyword.doc

    def run_keyword(self, name, *args, **kwargs):
        keyword = self.robot[name]
        return keyword(*args, **kwargs)

    def __getattr__(self, name):
        try:
            return self.robot[name]
        except KeyError:
            raise AttributeError(name)


TestLibrary = testlibrary()
keyword = TestLibrary.keyword


keyword(RobotRemoteServer.stop_remote_server)


class RemoteRobot(TestRobot, RobotRemoteServer, TestLibrary):
    def __init__(
      self, libraries, host='127.0.0.1', port=8270, port_file=None,
      allow_stop=True, allow_import=None,
      register_keywords=True, introspection=True,
      ):
        TestRobot.__init__(self, name='Remote', BuiltIn=False)
        TestLibrary.__init__(self)
        self.register_keywords = bool(register_keywords)
        self.introspection = bool(introspection)
        for lib in libraries:
            self.Import(lib)
        self.allow_import = list(allow_import or [])

        RobotRemoteServer.__init__(
          self, RemoteLibrary(robot=self),
          host, port, port_file, allow_stop)

    def _register_keyword(self, name, keyword):
        for funcname, func in [
          (name, keyword),
          (name + '.__repr__', keyword.__repr__),
          # To support IPython's ...? help system on xmlrpc.client side:
          (name + '.getdoc', lambda: keyword.__doc__),
          (name + '.__nonzero__', lambda: True),
          ]:
            self.register_function(func, funcname)

    def _register_library_keywords(self, lib):
        for keywordname in dir(lib):
            self._register_keyword(keywordname, self[keywordname])

    def _register_functions(self):
        RobotRemoteServer._register_functions(self)
        if self.register_keywords:
            for lib in self._libraries.values():
                self._register_library_keywords(lib)
        if self.introspection:
            self.register_introspection_functions()

    def get_keyword_names(self):
        return (self._library.get_keyword_names()
                + TestLibrary.get_keyword_names(self))

    def _get_keyword(self, name):
        try:
            keyword = self[name]
        except KeyError:
            try:
                return self.keywords[name]
            except KeyError:
                return None
        return keyword if type(keyword) is Keyword else None

    def _arguments_from_kw(self, keyword):
        if type(keyword) is Keyword:
            return list(keyword.arguments)
        return RobotRemoteServer._arguments_from_kw(self, keyword)

    def __dir__(self):
        return TestRobot.__dir__(self) + TestLibrary.__dir__(self)

    def __getattr__(self, name):
        try:
            return TestRobot.__getattr__(self, name)
        except AttributeError:
            return TestLibrary.__getattr__(self, name)


from . import keywords
