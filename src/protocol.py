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

"""Module containing various communication protocols."""

from collections import deque
from constants import PROTOCOL, SIMULATED

class Protocol(object):
    """Wrapper class to provide common interface for all communication 
protocols"""
    def __init__(self, attributeDict):
        if attributeDict[PROTOCOL] in available: # check if implemented
            self._config(attributeDict)
        else:
            raise IOError("{0} not implemented yet".format(attributeDict["PROTOCOL"]))

    def _config(self, attributeDict):
        """Create and configure backend device"""
        self.backend = available[attributeDict[PROTOCOL]](attributeDict)

    def open(self):
        """Open connection to backend"""
        self.backend.open()

    def isOpen(self):
        """Returns whether backend is open (True) or closed (False)"""
        return self.backend.isOpen()

    def close(self):
        """Close connection to backend"""
        self.backend.close()

    def read(self):
        """Read from backend buffer"""
        return self.backend.read()

    def write(self, message):
        """Write to backend buffer"""
        self.backend.write(message)


class Simulated(object):
    """Simulated communication with buffer which echos back commands"""
    def __init__(self, attributeDict):
        self.buffer = deque()
        self.status = False
        self.funcCallbacks = {}

    def open(self):
        self.status = True

    def isOpen(self):
        return self.status

    def close(self):
        self.status = False

    def write(self, string):
        if self.isOpen():
            self.buffer.append(string)
        else:
            raise IOError("Protocol not open")

    def read(self):
        if self.isOpen():
            try:
                func = self.buffer.popleft()
                if func in self.funcCallbacks.keys():
                    return self.funcCallbacks[func]()
            except IndexError:
                raise EmptyBufferError(self.buffer)
                
        else:
            raise IOError("Protocol not open")
        

class EmptyBufferError(Exception):
    def __init__(self, buffername):
        self.msg = "Nothing to read from empty buffer: {0}".format(buffername)

    def __str__(self):
        return self.msg


# available protocols
available = {SIMULATED : Simulated}

if __name__ == "__main__":
    attributeDict = {PROTOCOL: SIMULATED}
    p = Protocol(attributeDict)
    p.open()
