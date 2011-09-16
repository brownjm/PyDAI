#    PyDAI - Python Data Acquisition and Instrumentation
#
#    Copyright (C) 2011 Jeffrey M Brown, Greg A Cohoon, Kyle T Taylor
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import deque
import router
import devicemanager
import parser
import env
from constants import EXIT, EXEC, DEVMAN, ENV

class Executable(router.Node):
    def __init__(self):
        # commands specific to executable
        self.commands = {EXIT : self._exit}

        # create essential classes
        self.parser = parser.Parser(parser.commands, parser.rules)
        self.env = env.Environment()
        r = router.Router()
        devman = devicemanager.DeviceManager()

        # make connections to router
        r.connect(EXEC, self)
        r.connect(DEVMAN, devman)

    def run(self):
        raise Exception("Required to override")

    def execute(self, line):
        if line == EXIT:
            self.commands[EXIT]()
            return
        try:
            packet = self.parser.parse(line)
            self.router.send(packet)
        except parser.ParseError as pe:
            print pe

    def send(self, packet):
        raise Exception("Required to override")

    def doWelcome(self):
        print self.getWelcome()

    def getWelcome(self):
        return """
#    PyDAI
#
#    Copyright (C) 2011 Jeffrey M. Brown, Greg A Cohoon, Kyle T Taylor
#
#    Type 'exit' to quit.
"""

    def _exit(self):
        print "Goodbye!!"
