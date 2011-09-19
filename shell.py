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

from executable import Executable
from constants import EXIT, STATUS, NEW, DELETE, SOURCE, ERROR
import curses
import traceback
from collections import deque
from array import array

class CursesPrompt(Executable):
    def __init__(self):
        Executable.__init__(self)
        self.commands["view"] = self._view
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        self.yx = self.stdscr.getmaxyx()
        self.screen = curses.newwin(self.yx[0],self.yx[1],0,0)
        self.outputwin = self.screen.subwin(self.yx[0]-6, self.yx[1]-2, 3, 1)
        self.screen.keypad(1)
        self.screen.nodelay(1)
        self.screen.timeout(50)
        self.deviceWins = {"main": [False, array('c')]}
        self.currentWin = "main"

    def __get_input(self, prompt_string):
        self.inputwin.clear()
        self.inputwin.addstr(0,0,prompt_string)
        input = self.inputwin.getstr(0,len(prompt_string),60)
        self.inputwin.refresh()
        return input

    def __main_loop(self, prompt_string):
        input = array('c')

        while 1:
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
            elif i == curses.KEY_BACKSPACE:
                if len(input) > 0:
                    input.pop()
            elif i == curses.KEY_RESIZE:
                self.yx = self.stdscr.getmaxyx()
                self.screen.resize(self.yx[0],self.yx[1])
            elif not i == -1:
                try:
                    input.append(chr(i))
                except ValueError as ex:
                    self.addToOutput(self.currentWin, "Key entry error.")
            self.__update_screen(input.tostring())
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
        self.outputwin.addstr(0,0,self.deviceWins[self.currentWin][1].tostring())
        self.outputwin.noutrefresh()

    def addToOutput(self, win, outstr):
        self.deviceWins[win][1].fromstring(outstr)
        self.deviceWins[win][1].fromstring("\n")
        while self.deviceWins[win][1].count("\n") >= self.yx[0]-6:
            self.deviceWins[win][1].pop(0)
        if not win == self.currentWin:
            self.deviceWins[win][0] = True

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

    def _view(self, args):
        if args.args[0].lower() in self.deviceWins:
            if args.args[0] == self.currentWin:
                self.addToOutput(self.currentWin, "Already viewing {0}".format(args.args[0].title()))
            else:
                self.addToOutput(self.currentWin, "Switching to {0}".format(args.args[0].title()))
                self.deviceWins[args.args[0].lower()][0] = False
                self.currentWin = args.args[0].lower()
        else:
            self.addToOutput(self.currentWin, "Window {0} does not exist.".format(args.args[0]))

    def run(self):
        self.addToOutput("main", self.getWelcome())
        line = ''
        while line != EXIT:
            try:
                if len(line) > 0:
                    self.execute(line)

                line = self.__main_loop(">")
                self.env.addToHistory(line)
                self.addToOutput(self.currentWin, ''.join([">>> ", line]))
            except Exception as ex:
                self.addToOutput("main", "Error Occured:\n")
                self.addToOutput("main", traceback.format_exc())
                #raise ex
                line = ''

        curses.endwin()

    def _callback(self):
        pass

    def send(self, packet):
        if ERROR in packet.data:
            self.addToOutput(self.currentWin, packet[ERROR])
        else:
            self.addToOutput("main", repr(packet[STATUS]))
            if NEW in packet.data:
                self.deviceWins[packet[SOURCE]] = [False, array('c')]
                self.addToOutput(packet[SOURCE], repr(packet[STATUS]))
            if DELETE in packet.data:
                if self.currentWin == packet[SOURCE]:
                    self.currentWin = "main"
                self.deviceWins.pop(packet[SOURCE])

if __name__ == '__main__':
    try:
        CP = CursesPrompt()
        CP.run()
    except Exception as ex:
        curses.endwin()
        tb = traceback.format_exc()
        print "Catastrophic Error:\n"
        print tb
