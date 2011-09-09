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

"""Router class handles the transmission of Packets between all connected 
devices"""

class Packet(object):
    def __init__(self, source, dest, data):
        self.destination = dest
        self.source = source
        self.data = data

class Device(object):
    """Devices to be connected to Router"""
    def sendPacket(self, message):
        print message

class Router(object):
    def __init__(self):
        self.signals = {}

    def signal(self, device_name):
        for device in self.signals.get(device_name, []):
            handler(*args, **kwargs)

    def connect(self, signal_name, receiver):
        handlers = self.signals.setdefault(signal_name, [])
        handlers.append(receive)

    def disconnect(self, signal_name, receiver):
        handlers[signal_name].remove(receiver)


if __name__ == "__main__":
    r = Router()
