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

"""Unit test for parser.py"""

import unittest
from collections import deque
from src.parse import *
from src.router import Packet
from src.constants import *

p = Parser(commands, rules)
packet = Packet()

class ValidInput(unittest.TestCase):
    """Test that valid input produces correct commands and packets."""
    validStrings = (("new dev", 
                     [New], 
                     {"new":"dev", SOURCE:EXEC, TARGET:DEVMAN}, 
                     deque([DEVMAN])),

                    ("delete dev", 
                     [Delete],
                     {"delete":"dev", SOURCE:EXEC, TARGET:DEVMAN},
                     deque([DEVMAN])),

                    ("send data to dev", 
                     [Send, To],
                     {"send":"data", SOURCE:EXEC, TARGET:"dev"},
                     deque(["dev"])),

                    ("query dev", 
                     [Query],
                     {"query":"dev", SOURCE:EXEC, TARGET:"dev"},
                     deque(["dev"])),

                    ("exit", 
                     [Exit],
                     {},
                     deque([])),

                    ("help", 
                     [Help],
                     {},
                     deque([])),

                    ("help item", 
                     [Help],
                     {},
                     deque([])),

                    ("view dev", 
                     [View],
                     {},
                     deque([]))
                    )

    def testParse(self):
        """Test that valid input produces a valid command set."""
        for string, commandClass, data, dest in self.validStrings:
            result = p.parse(string)
            result = [type(item) for item in result]
            self.assertEqual(result, commandClass)

    def testPackage(self):
        """Test that valid command sets produce valid packets."""
        for string, commandClass, data, dest in self.validStrings:
            commandList = p.parse(string)
            result = p.package(commandList)
            self.assertEqual(result.data, data)
            self.assertEqual(result.dest, dest)


if __name__ == "__main__":
    unittest.main()
