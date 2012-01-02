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

"""Module containing the user environment."""

from collections import deque
import router
from constants import EXEC

class Environment(object):
    """Class to represent the user environment."""
    def __init__(self):
        self.history = []   # store command line history
        self.variables = {} # store user space variables
        self.index = 0
        self.length = 0

    def addToHistory(self, line):
        """Adds line to history"""
        if line != self.prev():
            self.history.append(line)

        self.index = self.length = len(self.history)

    def next(self):
        """Get next line from history"""
        if self.length == 0 or self.index == self.length:
            return ""
        if self.index < self.length:
            self.index += 1
        return self.history[self.index-1]
        
    def prev(self):
        """Get previous line from history"""
        if self.length == 0:
            return ""
        if self.index > 0:
            self.index -= 1
        return self.history[self.index]

    def addVariable(self, varname, var):
        """Store a variable"""
        self.variables[varname] = var

    def getVariable(self, varname):
        """Retrieve a variable"""
        return self.variables[varname]


if __name__ == "__main__":
    env = Environment()
    line = "hi how are you".split()
    for word in line:
        print word
        env.addToHistory(word)

    print "-----------------\n"
    for n in range(6):
        print env.prev()
