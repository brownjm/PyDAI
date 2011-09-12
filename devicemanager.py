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

class DeviceManager(router.Device):
    """Provides methods to handle installed devices."""
    def __init__(self):
        self.deviceList = dict()
        self.outbox = Queue.Queue()
        self.devFac = DeviceFactory()

    def send(self, packet):
        pass

    def addDevice(self, filename):
        self.deviceList[filename] = self.DevFac.constructDevice(filename)
       #self.DeviceList[filename].addDeviceManager(self)

if __name__ == '__main__':
    dm = DeviceManager(None)
#    dm.addDevice('dev1')
#    dm.addDevice('dev2')
#    dm.sendPacket(router.Packet('dev1', 'User', 'Command1'))
#    dm.sendPacket(router.Packet('dev1', 'User', 'Command2'))
#    dm.sendPacket(router.Packet('dev1', 'User', 'Command3'))
#    dm.sendPacket(router.Packet('dev2', 'User', 'Command1'))
#    dm.sendPacket(router.Packet('dev2', 'User', 'Command2'))
#    dm.sendPacket(router.Packet('dev2', 'User', 'Command3'))
