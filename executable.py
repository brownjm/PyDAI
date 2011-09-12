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

import router
import devicemanager
from collections import deque

class Executable(router.Device):
    def __init__(self):
        self.commands = {"exit" : self._exit, "blah" : self._blah}

        r = router.Router()
        router.Device.__init__(self, r)
        d = devicemanager.DeviceManager()
        d.router = self.router
        self.router.connect("EXEC", self)
        self.router.connect("DEVMAN", d)

    def run(self):
        raise Exception("Required to override")

    def execute(self, line):
        command = line.split(' ')[0]
        aftercommand = line.split(' ')[1:]
        if command in self.commands:
            self.commands[command]()
        else:
            print 'Command "' + command + '" not found.'

        return command

    def send(self, packet):
        raise Exception("Required to override")

    def doWelcome(self):
        print """
#    PyDAI
#
#    Copyright (C) 2011 Jeffery M. Brown, Greg A Cohoon, Kyle T Taylor
#
#    Type 'exit' to quit.
"""

    def _exit(self):
        print 'Goodbye!!'

    def _blah(self):
        d = deque()
        d.append("DEVMAN")
        p = router.Packet(d, 'TESTING')
        self.router.send(p)
