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

class Device(object):
    def __init__(self, attributeDict, commandDict={}):
        self.attribute = attributeDict
        self.command = commandDict
        self.commandPool = Queue.Queue()
        self.commandThread = ProcessThread(self)
        self.protocol = protocol.Protocol(attributeDict)

    def read(self):
        pass

    def write(self, packet):
        self.commandPool.put(packet.data)
        if not self.commandThread.isAlive():
            self.commandThread.start()

class ProcessThread(threading.Thread):
    def __init__(self, device):
        self.device = device
        threading.Thread.__init__(self)

    def run(self):
        while not self.device.commandPool.empty():
            command = self.device.commandPool.get()
            #Do something with command here!
            #Receive response from device and send back up chain.
            if not self.device.protocol.isOpen():
                self.device.protocol.open()
            self.device.protocol.write(command)

if __name__ == '__main__':
    d = Device({"PROTOCOL": "simulated"})
    d.write("Command1 Dev1")
    d.write("Command2 Dev1")
    d.write("Command3 Dev1")

    a = Device({"PROTOCOL": "simulated"})
    a.write("Command1 Dev2")
    a.write("Command2 Dev2")
    a.write("Command3 Dev2")

