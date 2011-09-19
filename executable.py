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

import sys
from collections import deque
import router
import devicemanager
import parser
import env
from constants import EXIT, EXEC, DEVMAN, ENV, HELP

class Executable(router.Node):
    def __init__(self):
        self.helper = Helper(parser.commands)
        # commands specific to executable
        self.commands = {EXIT : self._exit,
                         HELP : self.helper.help}

        # create essential classes
        self.parser = parser.Parser(parser.commands, parser.rules)
        self.env = env.Environment()
        r = router.Router()
        devman = devicemanager.DeviceManager()

        # make connections to router
        r.connect(EXEC, self)
        r.connect(DEVMAN, devman)

    def run(self):
        raise Exception("Required to override")

    def execute(self, line):
        try:
            commandList = self.parser.parse(line)
            handled = False
            for command in commandList:
                if command.name in self.commands:
                    self.commands[command.name](command)
                    handled = True

            if not handled:
                packet = self.parser.package(commandList)
                self.router.send(packet)
        except parser.ParseError as pe:
            raise pe

    def send(self, packet):
        raise Exception("Required to override")

    def doWelcome(self):
        print self.getWelcome()

    def getWelcome(self):
        return """
#    PyDAI
#
#    Copyright (C) 2011 Jeffrey M Brown, Greg A Cohoon, Kyle T Taylor
#
#    Type 'exit' to quit.
"""

    def _exit(self, *args):
        return "Goodbye!!"


class Helper(object):
    """Gives user access to command docstrings within PyDAI."""
    def __init__(self, commandDict):
        """Gets docstrings from dictionary of command names and associated 
classes."""
        self.commandDict = {}
        for name, commandClass in commandDict.iteritems():
            self.commandDict[name] = self._trim(commandClass.__doc__)

    def help(self, helpCommand):
        """Get help on the line"""
        if len(helpCommand.args) == 0:
            return self._helpmessage()
        else:
            return self._getDocstring(helpCommand.args[0])

    def _getDocstring(self, name):
        """Return information specific to an object"""
        if name in self.commandDict:
            return self.commandDict[name]
        else:
            return "No help for this command is available: {}".format(name)

    def _helpmessage(self):
        return "Here are the available commands:\n{}\nTo receive more info on a command: help [command]".format(self.commandDict.keys())

    def _trim(self, docstring):
        """Removes newlines, aligns indentations, removes whitespace. 
Code example from PEP257"""
        if not docstring:
            return ''
        # Convert tabs to spaces (following the normal Python rules)
        # and split into a list of lines:
        lines = docstring.expandtabs().splitlines()
        # Determine minimum indentation (first line doesn't count):
        indent = sys.maxint
        for line in lines[1:]:
            stripped = line.lstrip()
            if stripped:
                indent = min(indent, len(line) - len(stripped))
        # Remove indentation (first line is special):
        trimmed = [lines[0].strip()]
        if indent < sys.maxint:
            for line in lines[1:]:
                trimmed.append(line[indent:].rstrip())
        # Strip off trailing and leading blank lines:
        while trimmed and not trimmed[-1]:
            trimmed.pop()
        while trimmed and not trimmed[0]:
            trimmed.pop(0)
        # Return a single string:
        return '\n'.join(trimmed)


if __name__ == "__main__":
    h = Helper(parser.commands)
    
