#    PyDAI - Python Data Acquisition and Instrumentation
#
#    Copyright (C) 2012 Jeffrey M Brown, Greg A Cohoon, Kyle T Taylor
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
from constants import SEND, DELETE, EXEC, STATUS, TIMEOUT, ERROR, ROUTER
from constants import QUERY, NAME, MODEL, SN, RETURN, TYPE

class Device(router.Node):
    def __init__(self, attributeDict, commandDict={}):
        router.Node.__init__(self)
        self.attribute = attributeDict
        self.command = commandDict
        self.packetPool = Queue.Queue()
        self.protocol = protocol.Protocol(attributeDict)
        self.protocol.open()
    
    def process(self, packet):
        if SEND in packet.data:
            request = packet.data[SEND]
            if request in self.attribute:
                data = self.attribute[request]
                packet.addDest(self.name, EXEC)
                packet[RETURN] = data
                packet[TYPE] = "string"
                
            elif request.split()[0] in self.command:
                command, returnType = self.command[request.split()[0]]
                args = request.split()
                args.pop(0) # first word is the command
                print args, len(args)
                numargs = command.count("{}")
                if numargs == len(args):
                    command = command.format(*args) # insert args, if any
                    print command
                    self.write(command)
                    time.sleep(float(self.attribute[TIMEOUT]))
                    response = self.read()
                    packet.addDest(self.name, EXEC)
                    packet[RETURN] = response
                    packet[TYPE] = returnType
                else:
                    packet.addDest(self.name, EXEC)
                    msg = "Device command signature does not match any in configuration file.\nYou requested command: {}\nWith these arguments:  {}"
                    packet[ERROR] = msg.format(command, args)
                
            else:
                packet.addDest(self.name, EXEC)
                packet[ERROR] = "Not a valid command for {}: {}".format(self.name, request)
                
        elif DELETE in packet.data:
            pass
            
        elif QUERY in packet.data:
            packet.addDest(self.name, EXEC)
            att = self.attribute
            packet[STATUS] = "\n".join([att[NAME], att[MODEL], att[SN]])
            
        else:
            packet.addDest(self.name, EXEC)
            packet[ERROR] = "Not a valid command for {}: {}".format(self.name, request)

        if not self.router == None:
            self.sendToRouter(packet)

    def read(self):
        """Read data from the physical device via Protocol class."""
        return self.protocol.read()
        

    def write(self, message):
        """Write data to the physical device via Protocol class"""
        self.protocol.write(message)


if __name__ == "__main__":
    import parse
    import devicefactory
    p = parse.Parser(parse.commands, parse.rules)
    df = devicefactory.DeviceFactory()

    packet = p.package(p.parse("send data 1  3 4 to dev1"))
    dev1 = df.constructDevice("dev1")
    dev1.process(packet)
    print packet
