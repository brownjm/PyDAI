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

import threading
import Queue
import time, random
import protocol
import router

class Device(threading.Thread, router.Node):
    def __init__(self, attributeDict, commandDict={}):
        threading.Thread.__init__(self)
        self.name = ""
        self.attribute = attributeDict
        self.command = commandDict
        self.packetPool = Queue.Queue()
        self.protocol = protocol.Protocol(attributeDict)
        self.protocol.open()

    def send(self, packet):
        if packet.data == 'destroy':
            self.router.disconnect(self.name)
            packet.dest.append("EXEC")
            packet.data = "Device " + self.name + " removed."

    def read(self):
        pass

    def write(self, packet):
        self.packetPool.put(packet)
        if not self.isAlive():
            self.start()

    def run(self):
        while not self.packetPool.empty():
            packet = self.packetPool.get()
            self.protocol.write(packet.data)

        threading.Thread.__init__(self)

