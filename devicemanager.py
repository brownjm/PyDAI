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
import router
from devicefactory import DeviceFactory, FileNotFoundError
from constants import NEW, DEVMAN, EXEC, STATUS, DELETE, QUERY, ERROR

class DeviceManager(router.Node):
    """Provides methods to handle installed devices."""
    def __init__(self):
        self.deviceList = []
        self.outbox = Queue.Queue()
        self.devFac = DeviceFactory()

    def send(self, packet):
        if NEW in packet.data:
            name = packet.data[NEW]
            if name in self.deviceList:
                packet.addDest(DEVMAN, EXEC)
                msg = "Device already created with the name: {0}".format(name)
                packet[ERROR] = msg

            else:
                try:
                    self.addDevice(name, name)
                    packet.addDest(DEVMAN, EXEC)
                    packet[STATUS] = "Device created: {0}".format(name)

                except FileNotFoundError as ex:
                    packet.addDest(DEVMAN, EXEC)
                    packet[ERROR] = ex.msg

        elif DELETE in packet.data:
            name = packet.data[DELETE]
            if not name in self.deviceList:
                packet.addDest(DEVMAN, EXEC)
                msg = "Device does not exist: {0}".format(name)
                packet[ERROR] = msg
            else:
                self.removeDevice(name, packet)
                
        elif QUERY in packet.data:
            packet.addDest(DEVMAN, EXEC)
            packet[STATUS] = str(self.deviceList)
            
        else:
            packet.addDest(DEVMAN, EXEC)
            packet[ERROR] = "{} cannot do anything with packet:\n{}".format(DEVMAN, packet)

        self.router.send(packet)

    def addDevice(self, filename, username):
        d = self.devFac.constructDevice(filename)
        d.name = username
        self.router.connect(username, d)
        self.deviceList.append(username)
    
    def removeDevice(self, username, packet):
        packet.addDest(DEVMAN, username)
        self.deviceList.remove(username)
        self.router.send(packet)

if __name__ == '__main__':
    dm = DeviceManager()
