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
from constants import NEW, DEVMAN, EXEC, AUTO
from constants import STATUS, QUERY, ERROR, RETURN, KILL, DELETE, RUN
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
        if packet.command == KILL:
            self.procStop.set()

        if packet.command == NEW:
            name = packet.data
            if name in self.deviceList:
                packet.reflect()
                packet.status = "Device already created with the name: {0}".format(name)
                packet.error = True
                
            else:
                try:
                    self.addDevice(name, name)
                    packet.source = name
                    packet.target = EXEC
                    packet.status = "Device created: {0}".format(name)
                    
                except FileNotFoundError as ex:
                    packet.reflect()
                    packet.status = ex.msg
                    packet.error = True
                    
        elif packet.command == RUN:
            name = packet.data
            if name in self.deviceList:
                packet.reflect()
                packet.source = "Script {0} already running.".format(name)
                packet.error = True

            else:
                try:
                    self.addDevice(AUTO, name)
                    packet.source = name
                    packet.target = EXEC
                    packet.status = "Script running"

                except FileNotFoundError as ex:
                    packet.reflect()
                    packet.status = ex.msg
                    packet.error = True

        elif packet.command == DELETE:
            name = packet.data
            if not name in self.deviceList:
                packet.reflect()
                packet.status = "Device does not exist: {0}".format(name)
                packet.error = True
            else:
                self.removeDevice(name, packet)
                
        elif packet.command == QUERY:
            packet.reflect()
            packet.status = "Current devices connected:"
            packet.data = self.deviceList.keys()
            
        else:
            packet.reflect()
            packet.status = "{} cannot do anything with packet:\n{}".format(DEVMAN, packet)
            packet.error = True
            
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
        #packet.addDest(username, EXEC)
        packet.source = username
        packet.target = EXEC
        packet.status = "Device deleted: {}".format(username)
        self.deviceList.pop(username)

if __name__ == '__main__':
    dm = DeviceManager()
    dm.start()
