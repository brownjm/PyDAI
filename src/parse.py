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

"""Module to handle translating text input from user into valid Packets"""

from collections import deque
import router
from constants import EXEC, DEVMAN, NEW, DELETE, SEND, TO, QUERY
from constants import EXIT, KILL, HELP, VIEW

class Parser(object):
    """Creates packets from input strings"""
    def __init__(self, commands, rules):
        self.commands = commands
        self.rules = rules

    def parse(self, string):
        """Create a packet from the input string"""
        words = self._createWordList(string)
        commands = []
        while len(words) > 0:
            commands.append(self._constructCommand(words))
        return commands

    def package(self, commands):
        """Use commands to create a Packet"""
        if self._isValid(commands):
            packet = router.Packet()
            for command in commands:
                command.modPacket(packet)
            return packet
        else:
            names = [com.name for com in commands]
            raise ParseError("Not a valid command set: {0}".format(names))

    def _createWordList(self, string):
        """Find the words within given string and create a list."""
        words = string.split()
        return deque(words)
            
    def _constructCommand(self, wordList):
        """Create commands from words"""
        if wordList[0] in self.commands:
            return self.commands[wordList[0]](wordList)
        else:
            raise ParseError("Command not recognized: {0}".format(wordList[0]))

    def _isValid(self, commands):
        self.comType = set([type(com) for com in commands])
        return self.comType in rules


class ParseError(Exception):
    def __init__(self, message):
        self.msg = message
    def __str__(self):
        return self.msg


class Command(object):
    """Base class for all commands"""
    def __init__(self, wordList, nargs=1):
        self.name = wordList.popleft()
        self.nargs = nargs
        self.args = []
        if len(wordList) < nargs:
            msg = "Command '{0}' expected {1} argument(s) and received {2}"
            raise ParseError(msg.format(self.name, nargs, len(wordList)))

        for n in range(nargs):
            self.args.append(wordList.popleft())

    def modPacket(self, packet):
        raise ParseError("Cannot create a packet from: {}".format(self.name))

    def __str__(self):
        return "{}({})".format(self.name, self.args)

    def __eq__(self, other):
        """Equivalence is same command class and arguments"""
        return (type(self) == type(other)) and (self.args == other.args)


class New(Command):
    """Creates a new device from specified configuration file.
Usage: new [config filename]
"""
    def __init__(self, wordList):
        Command.__init__(self, wordList, 1)

    def modPacket(self, packet):
        packet.addDest(EXEC, DEVMAN)
        packet[self.name] = self.args[0]

class Delete(Command):
    """Removes the specified device.
Usage: delete [device name]"""
    def __init__(self, wordList):
        Command.__init__(self, wordList, 1)

    def modPacket(self, packet):
        packet.addDest(EXEC, DEVMAN)
        packet[self.name] = self.args[0]

class Send(Command):
    """Send a command to a device.
Usage: send [device command] to [device name]"""
    def __init__(self, wordList):
        Command.__init__(self, wordList, 1)

    def modPacket(self, packet):
        packet[self.name] = self.args[0]

class To(Command):
    """Sets the destination of a command.
Usage: send [device command] to [device name]"""
    def __init__(self, wordList):
        Command.__init__(self, wordList, 1)

    def modPacket(self, packet):
        packet.addDest(EXEC, self.args[0])

class Query(Command):
    """Request a device's information.
Usage: query [device name]"""
    def __init__(self, wordList):
        Command.__init__(self, wordList, 1)

    def modPacket(self, packet):
        dev = self.args[0]
        packet.addDest(EXEC, dev)
        packet[self.name] = dev

class Exit(Command):
    """Exits the program.
Usage: exit"""
    def __init__(self, wordList):
        Command.__init__(self, wordList, 0)

    def modPacket(self, packet):
        pass

class Kill(Command):
    """Kills PyDAI server and exits client.
Usage: kill"""
    def __init__(self, wordList):
        Command.__init__(self, wordList, 0)

    def modPacket(self, packet):
        pass

class Help(Command):
    """Provides helpful information about commands.
Usage: help or help [command name]"""
    def __init__(self, wordList):
        if len(wordList) == 1: # help with no arguments
            Command.__init__(self, wordList, 0)
        else:
            Command.__init__(self, wordList, 1)

    def modPacket(self, packet):
        pass

class View(Command):
    """Switches focus to specified window.
Usage: view [window name]"""
    def __init__(self, wordList):
        Command.__init__(self, wordList, 1)

    def modPacket(self, packet):
        pass


# dictionary of available commands
# user defined name:  associated class
commands = {NEW: New,
            DELETE: Delete,
            SEND: Send,
            TO: To,
            QUERY: Query,
            EXIT: Exit,
            KILL: Kill,
            HELP: Help,
            VIEW: View}

# sets of commands that constitute a complete packet
rules = [set([New]),
         set([Delete]),
         set([Send, To]),
         set([Query]),
         set([Exit]),
         set([Kill]),
         set([Help]),
         set([View])]


if __name__ == "__main__":
    p = Parser(commands, rules)
    
    com = p.parse("new dev1")
    packet = p.package(com)
