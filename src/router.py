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
from constants import QUERY, ROUTER, EXEC, STATUS, TARGET, SOURCE, ERROR, DELETE
from multiprocessing.connection import Listener, Client
import multiprocessing
import select
import time

class Packet(object):
    """Data bundle including destination information"""
    def __init__(self):
        self.dest = deque()
        self.data = {}

    def __str__(self):
        """Pretty print of Packet"""
        return "{0} | {1}".format(" -> ".join(self.dest), self.data)

    def __eq__(self, other):
        """Equivalence is same destinations and same data"""
        return (self.dest == other.dest) and (self.data == other.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, val):
        self.data[key] = val

    def addDest(self, source, target):
        """Add new destination into queue"""
        self.data[SOURCE] = source
        self.data[TARGET] = target
        self.dest.append(target)

    def next(self):
        """Return name of next destination"""
        return self.dest.popleft()


class Node(multiprocessing.Process):
    """Inherit from this class and overload send method to be connected to 
Router"""
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.name = ""
        self.in_packetQueue = Queue.Queue()
        self.out_packetQueue = Queue.Queue()
        self.router = None
        self.procStop = multiprocessing.Event()
        self._stop = threading.Event()

    def connect(self, address, key):
        self.router = Client(address, authkey=key)
        p = Packet()
        p.addDest(self.name, ROUTER)
        p[STATUS] = "register"
        self.rt = threading.Thread(target=self.__routerThread, args=())
        self.rt.daemon = True
        self.rt.start()
        self.sendToRouter(p)

    def disconnect(self):
        name = self.name
        packet = Packet()
        packet.addDest(name, EXEC)
        packet[DELETE] = name
        packet[STATUS] = "Device deleted: {}".format(name)
        self.sendToRouter(packet)
        self.router.close()
        self.router = None
        self._stop.set()
        self.rt.join()

    def process(self, packet):
        raise AttributeError("Must overload process method")

    def run(self):
        self.connect(('localhost', 15000), '12345')
        while not self.procStop.is_set():
            if not self.in_packetQueue.empty():
                packet = self.in_packetQueue.get()
                self.process(packet)
            else:
                time.sleep(.01)
                
        self.disconnect()

    def __routerThread(self):
        r = self.router
        while (not self._stop.isSet()):# or (not self.out_packetQueue.empty()):
            inr, outr, excr = select.select([r], [r], [], .1)
            for router_in in inr:
                p = router_in.recv()
                self.in_packetQueue.put(p)
            for router_out in outr:
                if not self.out_packetQueue.empty():
                    packet = self.out_packetQueue.get()
                    router_out.send(packet)

            time.sleep(.01)

    def sendToRouter(self, packet):
        self.out_packetQueue.put(packet)

class Router(multiprocessing.Process):
    """Routes Packets to appropriate Device"""
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.devTable = {} #Contains dict of connections to device processes
        self.server = Listener(('', 15000), authkey='12345')

    def run(self):
        running = 1
        tmpConnections = []
        while running:
            inputs = [self.server._listener._socket]
            inputs.extend(tmpConnections)
            inputs.extend(self.devTable.values())
            inr, outr, excr = select.select(inputs, [], [])
            for s in inr:
                if s == self.server._listener._socket:
                    #Connecting a client
                    conn = self.server.accept()
                    tmpConnections.append(conn)
                else:
                    try:
                        packet = s.recv()

                        #TODO: Add ability to gracefully KILL everything connected

                        if QUERY in packet.data and packet.data[QUERY] == ROUTER:
                            packet.next()
                            packet.addDest(ROUTER, EXEC)
                            packet[STATUS] = str(self.devTable.keys())
                        elif STATUS in packet.data and packet[STATUS] == "register":
                            #Registering a device
                            self.devTable[packet[SOURCE]] = s
                            tmpConnections.remove(s)
                            print "Device " + packet[SOURCE] + " registered"
                        
                        if packet.data[TARGET] == ROUTER:
                            continue

                        #Route to next
                        if packet.data[TARGET] not in self.devTable:
                            unknown = packet.next() #pop off unknonw target
                            packet.addDest(ROUTER, EXEC)
                            packet[ERROR] = "Target device not found: {}".format(unknown)
                            
                        self.devTable[packet.next()].send(packet)
                    except EOFError:
                        #Close connection
                        s.close()
                        if s in tmpConnections:
                            tmpConnections.remove(s)
                        
                        for dev in self.devTable.keys():
                            if self.devTable[dev] == s:
                                self.devTable.pop(dev)
                                print "Device " + dev + " removed."
                                break

    def connect(self, device_name, device):
        device.router = self
        self.devTable[device_name] = WorkerThread(device)
        self.devTable[device_name].router = self

    def disconnect(self, device_name):
        deviceThread = self.devTable.pop(device_name)
        deviceThread.disconnect()


if __name__ == "__main__":
    r = Router()
    r.start()
