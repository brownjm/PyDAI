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

"""Unit test for parser.py"""

import unittest
from .. import PyDAI
#p = PyDAI.src.parser.Parser(commands, rules)

class ValidInput(unittest.TestCase):
    """Test that valid input produces correct commands and packets."""
    validStrings = (("new dev", [New(["new", "dev"])]),
                    ("delete dev", [Delete(["delete", "dev"])]),
                    ("send data to dev", [Send(["send", "data"]), To("to", "dev")]),
                    ("query dev", [Query(["query", "dev"])]),
                    ("exit", [Exit(["exit"])]),
                    ("help", [Help(["help"])]),
                    ("help item", [Help(["help", "item"])]),
                    ("view dev", [View(["view", "dev"])])
                    )

    def testParse(self):
        """Test that valid input produces a valid command set."""
        for string, commands in self.validStrings:
            result = p.parse(string)
            self.assertEqual(result, commands)


if __name__ == "__main__":
    unittest.main()
