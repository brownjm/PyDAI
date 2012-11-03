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

import inspect
import sys
from collections import deque
import router
import devicemanager
import parse
import env
from constants import EXIT, STATUS, NEW, DELETE, SOURCE, ERROR, QUERY, RETURN, KILL, RUN, TYPE, SEND
from constants import EXEC, DEVMAN, ENV, HELP

DEBUG_FLAG = True

class Executable(router.Node):
    def __init__(self, address, akey):
        router.Node.__init__(self, address, akey)
        self.helper = Helper(parse.commands)
        # commands specific to executable
        self.commands = {EXIT : self._exit,
                         HELP : self.helper.help}

        # create essential classes
        self.parser = parse.Parser(parse.commands, parse.rules)
        self.env = env.Environment()

        self.name = EXEC
        self.connect(self.address, self.akey)
        self.deviceWins = {"main": [False, []]}
        self.currentWin = "main"

    def send(self, packet):
        raise Exception("Required to override")

    def doWelcome(self):
        print self.getWelcome()

    def getWelcome(self):
        return """#    PyDAI
#
#    Copyright (C) 2011 Jeffrey M Brown, Greg A Cohoon, Kyle T Taylor
#
#    Type 'exit' to quit."""

    def _exit(self, *args):
        self.disconnect()
        return "Goodbye!!"
        
    def addToOutput(self, win, outstr):
        raise AttributeError("Must overload process method")
        
    def handle_packets(self):
        if not self.in_packetQueue.empty():
            packet = self.in_packetQueue.get()
            output = ''
            if DEBUG_FLAG:
                output = "Received: {}\n".format(packet)
                    
            if packet.error == True:
                output = ''.join([output, \
                "Error:\n{}".format(packet.status)])
                    
            else:
                output = ''.join([output, packet.status])

                if packet.command == NEW or packet.command == RUN:
                    self.deviceWins[packet.source] = [False, []]

                if packet.command == DELETE:
                    if self.currentWin == packet.source:
                        self.currentWin = "main"
                    self.deviceWins.pop(packet.source)

                if packet.command == QUERY:
                    if packet.source == EXEC:
                        output = ''.join([output, \
                        "You want to query yourself?\nWhat does \
                         that even mean?"])
                    elif packet.source == DEVMAN:
                        if len(packet.data) == 0:
                            output = ''.join([output, "None"])
                        else:
                            packet.data.reverse()
                            output = ''.join([output, \
                            ''.join(packet.data)])
                            for dev in packet.data:
                                if not dev in self.deviceWins:
                                    self.deviceWins[dev] = [False, []]

                if packet.command == SEND:
                    if packet.source == EXEC:
                        output = ''.join([output, \
                        "Sending something to yourself?"])
                    elif packet.returnType == "string":
                        output = ''.join([output, packet.data])
                
                self.addToOutput("main", output)
                if self.currentWin != "main":
                    self.addToOutput(self.currentWin, output)
                    
                if self.currentWin != packet.source and \
                packet.source in self.deviceWins:
                    self.addToOutput(packet.source, output)

class Helper(object):
    """Gives user access to command docstrings within PyDAI."""
    def __init__(self, commandDict):
        """Gets docstrings from dictionary of command names and associated 
classes."""
        self.commandDict = {}
        for name, commandClass in commandDict.iteritems():
            self.commandDict[name] = inspect.getdoc(commandClass)

    def help(self, helpCommand):
        """Get help on the line"""
        if len(helpCommand.args) == 0:
            return self.helpmessage()
        else:
            return self.getDocstring(helpCommand.args[0])

    def getDocstring(self, name):
        """Return information specific to an object"""
        if name in self.commandDict:
            return self.commandDict[name]
        else:
            return "No help for this command is available: {}".format(name)

    def helpmessage(self):
        return "Here are the available commands:\n{}\nTo receive more info on a command: help [command]".format(self.commandDict.keys())


if __name__ == "__main__":
    h = Helper(parse.commands)
