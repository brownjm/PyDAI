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

from collections import deque
import router

class Parser(router.Node):
    """Creates packets from input strings"""
    def __init__(self, commands, rules):
        self.commands = commands
        self.rules = rules
        router.Node.__init__(self) # allows connection to Router class

    def parse(self, string):
        words = self._createWordList(string)
        commandSet = set()
        commandClasses = set()
        while len(words) > 0:
            command = self._constructCommand(words)
            commandSet.add(command) # set of command objects
            commandClasses.add(command.__class__) # set of corresponding class

        commandClasses = frozenset(commandClasses) # make hashable as key

        if commandClasses in rules:
            packetList = self._generatePackets(commandSet, rules[commandClasses])
            return packetList
        else:
            raise KeyError("Incomplete command set: {0}".format(commandSet))

    def _createWordList(self, string):
        """Find the words within given string and create a list."""
        words = string.split()
        return deque(words)
            
    def _constructCommand(self, wordList):
        """Create commands from words"""
        if wordList[0] in self.commands:
            return self.commands[wordList.popleft()](wordList)
        else:
            raise KeyError("Command not recognized: {0}".format(wordList[0]))

    def _generatePackets(self, commandSet, rule):
        packetList = []
        for packetRule in rule: # length of rule determines number of packets
            p = router.Packet()
            for commandClass in packetRule:
                for command in commandSet:
                    if isinstance(command, commandClass):
                        command.modPacket(p)

            packetList.append(p)

        return packetList


class Command(object):
    """Base class for all commands"""
    def __init__(self, wordList, nargs=1):
        self.nargs = nargs
        self.args = []
        if len(wordList) < nargs:
            raise Exception("Command {0} expected {1} argument(s) and received {2}".format(self.__class__, nargs, len(wordList)))
        for n in range(nargs):
            self.args.append(wordList.popleft())

    def modPacket(self, packet):
        raise Exception("Must overload how command modifies packet")

    def __str__(self):
        return str(self.__class__) + " : " + ", ".join(self.args)

class New(Command):
    """Create command a new object"""
    def __init__(self, wordList):
        Command.__init__(self, wordList, 1)

    def modPacket(self, packet):
        packet.dest = deque(["DEVMAN", "EXEC"])
        packet.data = self

class Delete(Command):
    """Deletion delete an object"""
    def __init__(self, wordList):
        Command.__init__(self, wordList, 1)

    def modPacket(self, packet):
        packet.dest = deque(["DEVMAN", "EXEC"])
        packet.data = self

class From(Command):
    """Sets packets packet destination"""
    def __init__(self, wordList):
        Command.__init__(self, wordList, 1)

    def modPacket(self, packet):
        packet.dest = deque([self.args[0], "EXEC"])

class Get(Command):
    """Sends message to device"""
    def __init__(self, wordList):
        Command.__init__(self, wordList, 1)

    def modPacket(self, packet):
        packet.data = self


# dictionary of available commands
# user defined name:  associated class
commands = {"new": New,
            "delete": Delete,
            "from": From,
            "get": Get}

# sets of commands that constitute a complete packets
# tuple of tuples to show grouping of commands into individual packets
rules = {frozenset([New]): [[New]],
         frozenset([Delete]): [[Delete]],
         frozenset([Get, From]): [[Get, From]]}


if __name__ == "__main__":
    p = Parser(commands, rules)
    packets = p.parse("get waveform from dev")
    print packets[0]
