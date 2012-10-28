#    PyDAI - Python Data Acquisition and Instrumentation
#
#    Copyright (C) 2012 Jeffrey M Brown, Greg A Cohoon, Kyle T Taylor
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distribdsfaduted in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Web class handles the transmission of data between the web server and 
the rest of PyDAI"""

from constants import EXIT, STATUS, NEW, DELETE, SOURCE, ERROR, QUERY
from constants import RETURN, KILL, RUN, TYPE, SEND, DEVMAN, EXEC
from executable import Executable
import router
import devicemanager
import time
from multiprocessing import Queue

class Webecutable(Executable):
    def __init__(self, address=('localhost', 15000), akey='12345', wInQueue=Queue(), wOutQueue=Queue()):
        Executable.__init__(self, address, akey)
        self.name = EXEC
        self.wInQueue = wInQueue
        self.wOutQueue = wOutQueue
        self.wOutQueue.put({'main' : self.formatOutput(self.getWelcome())})

    def formatOutput(self, string):
        return string.replace('\n', '<br/>')

    def run(self):
        while not self.procStop.is_set():
            if self.wInQueue.qsize() > 0:
                try:
                    line = str(self.wInQueue.get())
                    commandList = self.parser.parse(line)
                    packet = self.parser.package(commandList)
                    self.sendToRouter(packet)
                except EOFError:
                    #Do something here probably
                    pass

            if not self.in_packetQueue.empty():
                packet = self.in_packetQueue.get()
                if packet.command == QUERY:
                    returnStr = packet.status + '<br/>'
                    if packet.source == DEVMAN:
                        if len(packet.data) == 0:
                            returnStr = returnStr + "None"
                        else:
                            returnStr = returnStr + '<br/>'.join(packet.data)
                        self.wOutQueue.put({'main': self.formatOutput(returnStr)})

                if packet.command == NEW:
                    self.wOutQueue.put({packet.source : self.formatOutput(packet.status)})
                    self.wOutQueue.put({'main' : self.formatOutput(packet.status)})

            time.sleep(.01)

if __name__ == '__main__':
    from multiprocessing import Queue
    import threading
    r = router.Router()
    r.start()

    d = devicemanager.DeviceManager()
    d.start()
    
    a = Queue()
    b = Queue()
    w = Webecutable(wInQueue=a, wOutQueue=b)
    c = threading.Thread(target=w.run, args=())
    c.daemon = True
    c.start()
    time.sleep(1)
    print 'slept'
    a.put('query devman')
