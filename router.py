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
Nodes"""

from collections import deque
import threading
import Queue
from constants import QUERY, ROUTER, EXEC, STATUS, FROM

class Packet(object):
    """Data bundle including destination information"""
    def __init__(self):
        self.dest = deque()
        self.data = {}

    def __str__(self):
        """Pretty print of Packet"""
        return "{0} | {1}".format(" -> ".join(self.dest), self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, val):
        self.data[key] = val

    def addDest(self, destination):
        """Add new destination into queue"""
        self.data[FROM] = destination
        self.dest.append(destination)

    def next(self):
        """Return name of next destination"""
        return self.dest.popleft()


class Node(object):
    """Inherit from this class and overload send method to be connected to 
Router"""
    def __init__(self):
        self.router = None

    def send(self, packet):
        raise AttributeError("Must overload send method")


class Router(object):
    """Routes Packets to appropriate Device"""
    def __init__(self):
        self.devTable = {}

    def send(self, packet):
        """Send packet to next destination"""
        if len(packet.dest) == 0:
            return

        # check whether user is requesting info from Router itself
        if QUERY in packet.data:
            device = packet.data[QUERY]
            if device == ROUTER:
                packet.next() # pop off ROUTER
                packet.addDest(EXEC)
                packet[STATUS] = str(self.devTable.keys())

        if packet.data[FROM] not in self.devTable:
            unknown = packet.next() # pop off unknown query target
            packet.addDest(EXEC)
            packet[STATUS] = "Target device not found: {}".format(unknown)

        self.devTable[packet.next()].send(packet)

    def connect(self, device_name, device):
        device.router = self
        self.devTable[device_name] = WorkerThread(device)
        self.devTable[device_name].router = self

    def disconnect(self, device_name):
        deviceThread = self.devTable.pop(device_name)
        deviceThread.disconnect()


class WorkerThread(threading.Thread):
    def __init__(self, dev):
        threading.Thread.__init__(self)
        self.device = dev
        self.packetPool = Queue.Queue()

    def disconnect(self):
        self.device = None

    def send(self, packet):
        self.packetPool.put(packet)
        if not self.isAlive():
            self.start()

    def run(self):
        while not self.packetPool.empty():
            packet = self.packetPool.get();
            self.device.send(packet)
            if not len(packet.dest) == 0:
                self.router.send(packet)

        threading.Thread.__init__(self)

if __name__ == "__main__":
    # create router
    r = Router()

    # create a test device
    class testdev(Node):
        def __init__(self):
            Node.__init__(self)

        def send(self, packet):
            print packet
            if len(packet.dest) > 0:
                self.router.send(packet)

    a = testdev()
    b = testdev()
    c = testdev()

    # connect devices
    r.connect('a', a)
    r.connect('b', b)
    r.connect('c', c)

    # create packet
    p = Packet()
    p.addDest('a')
    p.addDest('b')
    p.addDest('c')
    p["data"] = 1

    # send initial packet to router
    r.send(p)
