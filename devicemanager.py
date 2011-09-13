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
from devicefactory import DeviceFactory

class DeviceManager(router.Node):
    """Provides methods to handle installed devices."""
    def __init__(self):
        self.deviceList = []
        self.outbox = Queue.Queue()
        self.devFac = DeviceFactory()

    def send(self, packet):
        command = packet.data.split(' ')[0]
        aftercommand = packet.data.split(' ')[1:]
        if command == 'create':
            dev = aftercommand[0]
            name = aftercommand[2]
            if name in self.deviceList:
                raise Exception("Device already created with the name " + name)
            self.addDevice(dev, name)
            packet.dest.append("EXEC")
            packet.data = "Device " + name + " created."
        elif command == 'destroy':
            name = aftercommand[0]
            if not name in self.deviceList:
                raise Exception("No device named " + name + " exists.")
            
            self.removeDevice(name, packet)
        elif command == 'query':
            packet.dest.append("EXEC")
            packet.data = self.deviceList
            

    def addDevice(self, filename, username):
        d = self.devFac.constructDevice(filename)
        d.name = username
        self.router.connect(username, d)
        self.deviceList.append(username)
    
    def removeDevice(self, username, packet):
        packet.dest.append(username)
        packet.data = 'destroy'
        self.deviceList.remove(username)

if __name__ == '__main__':
    dm = DeviceManager()
