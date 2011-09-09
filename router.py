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

from time import sleep
from collections import deque

class Packet(object):
    """Data bundle including destination information"""
    def __init__(self, destinations, data):
        if isinstance(destinations, deque): # make sure it is a deque
            self.dest = destinations
        else:
            raise TypeError("destinations must be a collections.deque")
        self.data = data

    def __str__(self):
        return "{0} : {1}".format(" -> ".join(self.dest), self.data)

    def next(self):
        """Return name of next destination"""
        return self.dest.popleft()


class Device(object):
    """Devices to be connected to Router"""
    def __init__(self, router):
        self.router = router

    def send(self, packet):
        # do something with packet
        print packet
        # done with packet
        if len(packet.dest) > 0:
            self.router.send(packet)


class Router(object):
    """Routes Packets to appropriate Device"""
    def __init__(self):
        self.devTable = {}

    def send(self, packet):
        """Send packet to next destination"""
        self.devTable[packet.next()].send(packet)

    def connect(self, device_name, device):
        self.devTable[device_name] = device

    def disconnect(self, device_name, device):
        self.devTable[device_name].pop()


if __name__ == "__main__":
    # create router
    r = Router()

    # create devices, they need a ref to router in order to return packet
    a = Device(r)
    b = Device(r)
    c = Device(r)

    # connect devices
    r.connect('a', a)
    r.connect('b', b)
    r.connect('c', c)

    # create packet
    n = 3 # number of round trips
    p = Packet(deque(['a', 'b', 'c']*n), "data")

    # send initial packet to router
    r.send(p)
