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
from devicefactory import DeviceFactory
from packet import Packet

class DeviceManager(object):
    """Provides methods to handle installed devices."""
    def __init__(self, router):
        self.DeviceList = dict()
        self.Outbox = Queue.Queue()
        self.Router = router
        self.DevFac = DeviceFactory()

    def addDevice(self, filename):
        self.DeviceList[filename] = self.DevFac.constructDevice(filename)
        self.DeviceList[filename].addDeviceManager(self)

    def sendPacket(self, packet):
        self.DeviceList[packet.Destination].addPacket(packet)

    def sendResponse(self, packet):
        self.Outbox.put(packet)
        print packet.Source, packet.Data

if __name__ == '__main__':
    dm = DeviceManager(None)
    dm.addDevice('Dev1')
    dm.addDevice('Dev2')
    dm.sendPacket(Packet('Dev1', 'User', 'Command1'))
    dm.sendPacket(Packet('Dev1', 'User', 'Command2'))
    dm.sendPacket(Packet('Dev1', 'User', 'Command3'))
    dm.sendPacket(Packet('Dev2', 'User', 'Command1'))
    dm.sendPacket(Packet('Dev2', 'User', 'Command2'))
    dm.sendPacket(Packet('Dev2', 'User', 'Command3'))
