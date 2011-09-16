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

"""Module containing the user environment."""

from collections import deque
import router
from constants import EXEC

class Environment(router.Node):
    """Class to represent the user environment."""
    def __init__(self):
        self.history = deque() # store command line history
        self.variables = {}    # store user space variables

    def addToHistory(self, line):
        """Adds line to history"""
        self.history.appendleft(line)

    def getFromHistory(self, index):
        """Get a line from history"""
        if len(self.history) == 0:
            return ""

        elif index >= len(self.history):
            return self.history[-1]

        else:
            return self.history[index]

    def addVariable(self, varname, var):
        """Store a variable"""
        self.variables[varname] = var

    def getVariable(self, varname):
        """Retrieve a variable"""
        return self.variables[varname]

    def send(self, packet):
        # just send a response that packet was received
        packet.addDest(EXEC)
        packet[STATUS] = "Packet received"
        self.router.send(packet)

if __name__ == "__main__":
    env = Environment()
    line = "hi how are you".split()
    for word in line:
        print word
        env.addToHistory(word)

    print "-----------------\n"
    for n in range(6):
        print env.getFromHistory(n)
