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

"""Module containing various communication protocols."""

from collections import deque

class Protocol(object):
    """Wrapper class to provide common interface for all communication 
protocols"""
    def __init__(self, name="simulated"):
        if name in available:
            self.name = name
        else:
            raise IOError("{0} not implemented yet".format(name))

    def config(self, **kwargs):
        """Create and configure backend device"""
        self.backend = available[self.name](**kwargs)

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

    def write(self, string):
        """Write to backend buffer"""
        if isinstance(string, str):
            self.backend.write(string)
        else:
            raise TypeError("{0} is not a string".format(string))


class Simulated(object):
    """Simulated communication with buffer which echos back commands"""
    def __init__(self, **kwargs):
        self.buffer = deque()
        self.status = False

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
            return self.buffer.popleft()
        else:
            raise IOError("Protocol not open")
        

# available protocols
available = {"simulated" : Simulated}

if __name__ == "__main__":
    p = Protocol("simulated")
    p.config()
    p.open()
