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

import Queue
import time, random
import protocol
import router
from constants import GET, DELETE, EXEC, STATUS

class Device(router.Node):
    def __init__(self, attributeDict, commandDict={}):
        self.name = ""
        self.attribute = attributeDict
        self.command = commandDict
        self.packetPool = Queue.Queue()
        self.protocol = protocol.Protocol(attributeDict)
        self.protocol.open()

    def send(self, packet):
        if GET in packet.data:
            com = self.command[packet.data[GET]]
            # incomplete
            
        elif DELETE in packet.data:
            name = packet.data[DELETE]
            self.router.disconnect(name)
            packet.addDest(EXEC)
            packet[STATUS] = "Device deleted: {0}".format(name)

    def read(self):
        pass

    def write(self, packet):
        pass

