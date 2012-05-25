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

from executable import Executable
from constants import EXIT, STATUS, NEW, DELETE, SOURCE, ERROR, QUERY, RETURN, KILL
from constants import EXEC, DEVMAN
import curses
import traceback
from collections import deque
from array import array

DEBUG_FLAG = True

class CursesPrompt(Executable):
    def __init__(self, address=('localhost', 15000), akey='12345'):
        Executable.__init__(self, address, akey)
        self.commands["view"] = self._view
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        self.yx = self.stdscr.getmaxyx()
        self.screen = curses.newwin(self.yx[0],self.yx[1],0,0)
        self.outputwin = self.screen.subwin(self.yx[0]-6, self.yx[1]-2, 3, 1)
        self.screen.keypad(1)
        self.screen.nodelay(1)
        self.screen.timeout(50)
        self.deviceWins = {"main": [False, []]}
        self.currentWin = "main"
        self.topLine = 0

    def __main_loop(self, prompt_string):
        input = array('c')

        while not self.procStop.is_set():
            i = self.screen.getch(self.yx[0]-2, len(input))
            if i == curses.KEY_ENTER or i == 10:
                break
            elif i == curses.KEY_UP:
                hist = self.env.prev()
                input = array('c')
                input.fromstring(hist)
            elif i == curses.KEY_DOWN:
                hist = self.env.next()
                input = array('c')
                input.fromstring(hist)
            elif i == curses.KEY_LEFT or i == curses.KEY_RIGHT:
                pass
            elif i == 554 or i == 539:
                #Control-Right or Control-Left
                self._movewin(i)
            elif i == 519 or i == 560:
                #Control-Down or Control-Up
                self._scrollwin(i)
            elif i == curses.KEY_BACKSPACE or i == 127:
                if len(input) > 0:
                    input.pop()
            elif i == curses.KEY_RESIZE:
                self.yx = self.stdscr.getmaxyx()
                self.screen.resize(self.yx[0],self.yx[1])
                self.outputwin.resize(self.yx[0]-6, self.yx[1]-2)
                self._resetScroll()
            elif not i == -1:
                try:
                    input.append(chr(i))
                except ValueError as ex:
                    self.addToOutput(self.currentWin, "Key entry error.")
            self.__update_screen(input.tostring())
            self.__handle_packets()
            curses.doupdate()

        return input.tostring()

    def __update_screen(self, inp):
        self.screen.clear()
        self.screen.box()
        self.screen.hline(2,1,curses.ACS_HLINE,self.yx[1]-2)
        self.screen.hline(self.yx[0]-3,1,curses.ACS_HLINE,self.yx[1]-2)

        left = 2
        header = self.deviceWins.keys()
        header.reverse()
        for win in header:
            if self.currentWin == win:
                self.screen.addstr(1, left, win.title(), curses.A_UNDERLINE)
            elif self.deviceWins[win][0] == True:
                self.screen.addstr(1, left, win.title(), curses.A_REVERSE)
            else:
                self.screen.addstr(1, left, win.title())
            left = left + len(win) + 3

        self.screen.addstr(self.yx[0]-2,1,">")

        self.__update_display()
        self.__update_input(inp)
            
        self.screen.noutrefresh()

    def __update_input(self, dispStr):
        self.screen.addstr(self.yx[0] - 2, 3, dispStr)
        self.screen.addstr(self.yx[0] - 2, len(dispStr) + 3, ' ', curses.A_REVERSE)

    def __update_display(self):
        self.outputwin.clear()
        dispyx = self.outputwin.getmaxyx()
        top = self.topLine
        bot = top + dispyx[0]
        for index, line in enumerate(self.deviceWins[self.currentWin][1][top:bot]):
            if len(line) > dispyx[1]:
                self.outputwin.addstr(index,0,line[0:dispyx[1]-3])
            else:
                self.outputwin.addstr(index,0,line)


        winLen = len(self.deviceWins[self.currentWin][1])
        if winLen > dispyx[0]:
            currScrollLine = float(0)
            linesPerSect = 0
            totScroll = float(dispyx[0]) #Scroll from 0 to totScroll - 1
            xtraLines = float(winLen - totScroll)
            if self.topLine == int(xtraLines):
                currScrollLine = totScroll - 1
            else:
                linesPerSect = totScroll / xtraLines
                currScrollLine = float(self.topLine) * linesPerSect
            
            for y in range(0,int(totScroll)):
                if y == int(currScrollLine):
                    self.outputwin.addch(y, dispyx[1]-2, curses.ACS_DIAMOND)
                else:
                    self.outputwin.addch(y, dispyx[1]-2, curses.ACS_CKBOARD)

        self.outputwin.noutrefresh()

    def addToOutput(self, win, outstr):
        if outstr == None or outstr == '':
            return

        winLen = len(self.deviceWins[win][1])
        listToAdd = outstr.split('\n')
        newLen = len(listToAdd)
        self.deviceWins[win][1].extend(listToAdd)

        if not win == self.currentWin:
            self.deviceWins[win][0] = True
        else:
            if (winLen - (self.yx[0] - 6)) - self.topLine == 0 or \
            (winLen < self.yx[0]-6 and winLen + newLen > self.yx[0] - 6):
                self.topLine = (winLen - (self.yx[0] - 6)) + newLen

    def _movewin(self, direction):
        wins = self.deviceWins.keys()
        if len(wins) == 1:
            return

        wins.reverse()
        cw = wins.index(self.currentWin)
        if direction == 554:
            cw = cw + 1
        elif direction == 539:
            cw = cw - 1
        if cw >= 0 and cw < len(wins):
            self.currentWin = wins[cw]
            self.deviceWins[self.currentWin][0] = False
            self._resetScroll()

    def _resetScroll(self):
        winLen = len(self.deviceWins[self.currentWin][1])
        dispLen = self.outputwin.getmaxyx()[0]
        if winLen > dispLen:
            self.topLine = winLen - dispLen
        else:
            self.topLine = 0

    def _scrollwin(self, direction):
        winLen = len(self.deviceWins[self.currentWin][1])
        if winLen > self.yx[0] - 6:
            if direction == 519 and self.topLine < (winLen - (self.yx[0] - 6)):
                self.topLine = self.topLine + 1
            elif direction == 560 and self.topLine > 0:
                self.topLine = self.topLine - 1

    def _view(self, args):
        if args.args[0].lower() in self.deviceWins:
            if args.args[0] == self.currentWin:
                self.addToOutput(self.currentWin, "Already viewing {0}".format(args.args[0].title()))
            else:
                self.deviceWins[args.args[0].lower()][0] = False
                self.currentWin = args.args[0].lower()
                self._resetScroll()
        else:
            self.addToOutput(self.currentWin, "Window {0} does not exist.".format(args.args[0]))
        return ''

    def run(self):
        self.addToOutput("main", self.getWelcome())
        commandList = self.parser.parse("query devman")
        packet = self.parser.package(commandList)
        self.sendToRouter(packet)
        line = ''
        while not self.procStop.is_set():
            try:
                line = self.__main_loop(">")
                self.env.addToHistory(line)
                self.addToOutput(self.currentWin, ''.join(["\n>>> ", line]))

                if not line.strip() == '': # if line has chars other than whitespace
                    commandList = self.parser.parse(line)
                    handled = False
                    for command in commandList:
                        if command.name in self.commands:
                            self.addToOutput(self.currentWin, self.commands[command.name](command))
                            handled = True
                        
                    if not handled:
                        packet = self.parser.package(commandList)
                        if DEBUG_FLAG:
                            self.addToOutput(self.currentWin, "Sent: {}".format(packet))
                        self.sendToRouter(packet)
            except Exception as ex:
                self.addToOutput(self.currentWin, "Error Occured:\n")
                self.addToOutput(self.currentWin, traceback.format_exc())
                line = ''
        
        if not line == EXIT:
            self.addToOutput(self.currentWin, "Server Shut Down...\nPress any key to exit...")
            self.procStop.set()
            self.screen.nodelay(0)
            self.__update_screen('')
            curses.doupdate()
            i = self.screen.getch(self.yx[0]-2, 0)

        curses.endwin()

    def __handle_packets(self):
        if not self.in_packetQueue.empty():
            packet = self.in_packetQueue.get()
            if DEBUG_FLAG:
                self.addToOutput(self.currentWin, "Received: {}".format(packet))
            if ERROR in packet.data:
                self.addToOutput(self.currentWin, packet[ERROR])
            else:
                if STATUS in packet.data:
                    self.addToOutput("main", str(packet[STATUS]))

                if NEW in packet.data:
                    self.deviceWins[packet[SOURCE]] = [False, []]
                    self.addToOutput(packet[SOURCE], repr(packet[STATUS]))

                if DELETE in packet.data:
                    if self.currentWin == packet[SOURCE]:
                        self.currentWin = "main"
                    self.deviceWins.pop(packet[SOURCE])

                if QUERY in packet.data:
                    if packet[SOURCE] == EXEC:
                        self.addToOutput(self.currentWin, "You want to query yourself?\nWhat does that even mean?")
                    elif packet[SOURCE] == DEVMAN:
                        if len(packet[RETURN]) == 0:
                            self.addToOutput(self.currentWin, "None")
                        else:
                            packet[RETURN].reverse()
                            for dev in packet[RETURN]:
                                self.addToOutput(self.currentWin, dev)
                                if not dev in self.deviceWins:
                                    self.deviceWins[dev] = [False, []]
                    

if __name__ == '__main__':
    try:
        CP = CursesPrompt()
        CP.run()
    except Exception as ex:
        #curses.endwin()
        tb = traceback.format_exc()
        print "Catastrophic Error:\n"
        print tb
