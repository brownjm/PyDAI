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


# The whole idea with this class is to abstract away file system
# operations into simple commands for managing data from devices.
# DataManager will handle data in either a directory tree or some
# other clever file/data system and allow the user to save, load, 
# and finally export their data. Export means that they can save 
# it to another location outside of pydai's data system, such as
# their laptop's Documents folder.

class DataManager(router.Node):
    """Provides methods to handle data input and output"""
    def __init__(self, address=('localhost', 15000), akey='12345'):
        router.Node.__init__(self, address, akey)
        self.name = DATAMAN
        self.outbox = Queue.Queue()
        self.datafolder = DATAFOLDER

    def process(self, packet):
        # do stuff with packet
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


    # user commands
    def delete(self, dataname):
        # TODO: add command to parser
        # DELETE <pseudo filename>
        pass

    def export(self, dataname, filename):
        # TODO: add command to parser
        # EXPORT <pseudo filename> TO <OS full path filename>
        pass

    def open(self, dataname):
        # TODO: add command to parser
        # OPEN <pseudo filename>
        pass

    def save(self, dataname, filename):
        # TODO: add command to parser
        # SAVE <data name> AS <pseudo filename>
        pass


dataFileHeader = {"title":"", "date":"", "dataType":"", "dimensions":""}

