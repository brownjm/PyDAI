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

import os
import Queue
import router
from constants import DATAMAN, DATAFOLDER

class DataManager(router.Node):
    """Provides methods to handle data input and output"""
    def __init__(self, address=('localhost', 15000), akey='12345'):
        router.Node.__init__(self, address, akey)
        self.name = DATAMAN
        self.outbox = Queue.Queue()
        self.datafolder = DATAFOLDER

    def process(self, packet):
        # possible actions: save data, remove data entry, display entries

        packet.reflect()
        packet.status = "Didn't do anything"
        self.sendToRouter(packet)


    def listDataFiles(self, top):
        filelist = []
        for root, dirs, files in os.walk(top):
            for f in files:
                if f.endswith(".dat"):
                    fileList.append(os.path.join(root, f))
        return filelist
            
    def makeDirectory(self, dirname):
        os.mkdir(dirname)

    def copy(self):
        pass

    def rename(self):
        pass

    def delete(self):
        pass

    def save(self):
        pass


dataFileHeader = {"title":"", "date":"", "dataType":"", "dimensions":""}

