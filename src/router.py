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

"""Router class handles the transmission of Packets between all connected 
Nodes"""

import threading
import Queue
from multiprocessing.connection import Listener, Client
import multiprocessing
import select
import time
import traceback
from constants import ROUTER, DEVMAN, EXEC, TARGET, SOURCE
from constants import QUERY, STATUS, ERROR, DELETE, KILL, REGISTER

class Packet(object):
    """Data bundle including destination information"""
    def __init__(self, source="", target="", command="", status="", error=False,
                 data="", returnType=""):
        self.source = source
        self.target = target
        self.command = command
        self.status = status
        self.error = error
        self.data = data
        self.returnType = returnType
        
    def __str__(self):
        """Pretty print of Packet"""
        d = dict(self.__dict__) # make a copy so we don't destroy data
        return "{} -> {} | {}".format(d.pop("source"), d.pop("target"), d)

    def reflect(self):
        """Swap the source and target of a packet"""
        self.source, self.target = self.target, self.source

   
class Node(multiprocessing.Process):
    """Inherit from this class and overload send method to be connected to 
Router"""
    def __init__(self, address=('localhost', 15000), akey='12345'):
        multiprocessing.Process.__init__(self)
        self.address = address
        self.akey = akey
        self.name = ""
        self.in_packetQueue = Queue.Queue()
        self.out_packetQueue = Queue.Queue()
        self.router = None
        self.procStop = multiprocessing.Event()

    def connect(self, address, key):
        self.router = Client(address, authkey=key)
        p = Packet(source=self.name, target=ROUTER, command=REGISTER)
        self.rt = threading.Thread(target=self.__routerThread, args=())
        self.rt.daemon = True
        self.rt.start()
        self.sendToRouter(p)

    def disconnect(self):
        name = self.name
        packet = Packet(source=self.name, target=EXEC, 
                        command=DELETE, data=self.name, 
                        status="Device deleted: {}".format(name))
        self.sendToRouter(packet)
        self.router.close()
        self.router = None
        if not self.procStop.is_set():
            self.procStop.set()
        self.rt.join()

    def process(self, packet):
        raise AttributeError("Must overload process method")

    def run(self):
        self.connect(self.address, self.akey)
        while not self.procStop.is_set():
            if not self.in_packetQueue.empty():
                packet = self.in_packetQueue.get()
                try:
                    self.process(packet)
                except Exception as ex:
                    # catch unexpected errors and report with packets
                    packet.error = True
                    packet.status = traceback.format_exc(ex)
                    packet.source = self.name
                    packet.target = EXEC
                    self.sendToRouter(packet)
            else:
                time.sleep(.01)
                
        self.disconnect()

    def __routerThread(self):
        r = self.router
        while not self.procStop.is_set():
            inr, outr, excr = select.select([r], [r], [], .1)
            try:
                for router_in in inr:
                    p = router_in.recv()
                    self.in_packetQueue.put(p)
            except EOFError:
                #Handles unexpected close from router
                self.procStop.set()
                break

            for router_out in outr:
                if not self.out_packetQueue.empty():
                    if not self.procStop.is_set():
                        packet = self.out_packetQueue.get()
                        router_out.send(packet)

            time.sleep(.01)

    def sendToRouter(self, packet):
        self.out_packetQueue.put(packet)

class Router(multiprocessing.Process):
    """Routes Packets to appropriate Device"""
    def __init__(self, address=('', 15000), akey='12345'):
        multiprocessing.Process.__init__(self)
        self.devTable = {} #Contains dict of connections to device processes
        self.server = Listener(address, authkey=akey)
        self.procStop = multiprocessing.Event()

    def run(self):
        tmpConnections = []
        while not self.procStop.is_set():
            inputs = [self.server._listener._socket]
            inputs.extend(tmpConnections)
            inputs.extend(self.devTable.values())
            inr, outr, excr = select.select(inputs, [], [], .01)
            for s in inr:
                if s == self.server._listener._socket:
                    #Connecting a client
                    conn = self.server.accept()
                    tmpConnections.append(conn)
                else:
                    try:
                        packet = s.recv()
                        if packet:
                            self.__handle_packet(s, packet, tmpConnections)
                    except EOFError:
                        #Close connection
                        s.close()
                        if s in tmpConnections:
                            tmpConnections.remove(s)
                        
                        for dev in self.devTable.keys():
                            if self.devTable[dev] == s:
                                self.devTable.pop(dev)
                                #print "Device " + dev + " removed."
                                break

    def __handle_packet(self, s, packet, t):
        if packet.command == KILL:
            packet.source = ROUTER
            packet.target = DEVMAN
            self.procStop.set()

        if packet.command == QUERY and packet.data == ROUTER:
            packet.reflect()
            packet.status = str(self.devTable.keys())

        elif packet.command == REGISTER:
            #Registering a device
            self.devTable[packet.source] = s
            t.remove(s)
            #print "Device " + packet[SOURCE] + " registered"
                        
        if packet.target == ROUTER:
            return

        #Route to next
        if packet.target not in self.devTable:
            packet.target = EXEC
            packet.source = ROUTER
            packet.status = "Target device not found: {}".format(unknown)
            packet.error = True

        if not self.procStop.is_set():
            self.devTable[packet.target].send(packet)


if __name__ == "__main__":
    r = Router()
    r.start()
