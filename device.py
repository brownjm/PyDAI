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
from constants import GET, DELETE, EXEC, STATUS, TIMEOUT
from constants import QUERY, NAME, MODEL, SN, RETURN, TYPE

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
            request = packet.data[GET]
            if request in self.attribute:
                data = self.attribute[request]
                packet.addDest(EXEC)
                packet[RETURN] = data

            elif request in self.command:
                com, returnType = self.command[packet.data[GET]]
                self.write(com)
                time.sleep(float(self.attribute[TIMEOUT]))
                response = self.read()
                packet.addDest(EXEC)
                packet[STATUS] = response
                packet[TYPE] = returnType

            else:
                packet.addDest(EXEC)
                packet[STATUS] = "Dear User,\nI have no idea what you want me to do with this: {}\nSincerly,\n{}".format(request, self.name)
                #packet[STATUS] = "Not a valid command for {}: {}".format(self.name, request)
            
        elif DELETE in packet.data:
            name = packet.data[DELETE]
            self.router.disconnect(name)
            packet.addDest(EXEC)
            packet[STATUS] = "Device deleted: {}".format(name)

        elif QUERY in packet.data:
            packet.addDest(EXEC)
            att = self.attribute
            packet[STATUS] = "\n".join([att[NAME], att[MODEL], att[SN]])

        else:
            packet.addDest(EXEC)
            packet[STATUS] = "Congrats! You have gotten {} through all layers off security.\n-{}".format(request, self.name)

        self.router.send(packet)
            

    def read(self):
        """Read data from the physical device via Protocol class."""
        return self.protocol.read()
        

    def write(self, message):
        """Write data to the physical device via Protocol class"""
        self.protocol.write(message)

