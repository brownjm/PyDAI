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
import router
from devicefactory import DeviceFactory, FileNotFoundError
from constants import NEW, DEVMAN, EXEC
from constants import STATUS, QUERY, ERROR, RETURN, KILL, DELETE
import multiprocessing

class DeviceManager(router.Node):
    """Provides methods to handle installed devices."""
    def __init__(self, address=('localhost', 15000), akey='12345'):
        router.Node.__init__(self, address, akey)
        self.name = DEVMAN
        self.deviceList = dict()
        self.outbox = Queue.Queue()
        self.devFac = DeviceFactory()

    def process(self, packet):
        if KILL in packet.data:
            self.procStop.set()

        if NEW in packet.data:
            name = packet.data[NEW]
            if name in self.deviceList:
                packet.addDest(DEVMAN, EXEC)
                msg = "Device already created with the name: {0}".format(name)
                packet[ERROR] = msg
                
            else:
                try:
                    self.addDevice(name, name)
                    packet.addDest(name, EXEC)
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
            packet[STATUS] = "Current devices connected:"
            packet[RETURN] = self.deviceList.keys()
            
        else:
            packet.addDest(DEVMAN, EXEC)
            packet[ERROR] = "{} cannot do anything with packet:\n{}".format(DEVMAN, packet)
            
        self.sendToRouter(packet)

    def addDevice(self, filename, username):
        d = self.devFac.constructDevice(filename)
        self.deviceList[username] = (d, multiprocessing.Event())
        d.name = username
        d.address = self.address
        d.akey = self.akey
        d.daemon = True
        d.procStop = self.deviceList[username][1]
        d.start()
    
    def removeDevice(self, username, packet):
        d = self.deviceList[username][0]
        d.procStop.set()
        d.join()
        packet.addDest(username, EXEC)
        packet[STATUS] = "Device deleted: {}".format(username)
        self.deviceList.pop(username)

if __name__ == '__main__':
    dm = DeviceManager()
    dm.start()
