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

import threading
import Queue
import time, random

class Device(object):
    def __init__(self):
        self.CommandPool = Queue.Queue()
        self.CommandThread = ProcessThread(self)

    def addCommand(self, command):
        self.CommandPool.put(command)
        if not self.CommandThread.isAlive():
            self.CommandThread.start()

class ProcessThread(threading.Thread):
    def __init__(self, device):
        self.device = device
        threading.Thread.__init__(self)

    def run(self):
        while not self.device.CommandPool.empty():
            command = self.device.CommandPool.get()
            #Do something with command here!
            #Receive response from device and send back up chain.
            time.sleep(random.randint(1,5))
            print command            

if __name__ == '__main__':
    d = Device()
    d.addCommand("Command1 Dev1")
    d.addCommand("Command2 Dev1")
    d.addCommand("Command3 Dev1")

    a = Device()
    a.addCommand("Command1 Dev2")
    a.addCommand("Command2 Dev2")
    a.addCommand("Command3 Dev2")

