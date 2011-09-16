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
from constants import EXIT, STATUS
import curses
import traceback
from collections import deque
from array import array

class CursesPrompt(Executable):
    def __init__(self):
        Executable.__init__(self)
        self.history = deque([], 10)
        self.screen = curses.initscr()
        self.yx = self.screen.getmaxyx()
        self.inputwin = curses.newwin(1, self.yx[1], self.yx[0]-1, 0)
        self.outputwin = curses.newwin(self.yx[0]-1, self.yx[1], 0, 0)
        self.outputwin.leaveok(1)
        self.outputbuffer = array('c')

    def __get_input(self, prompt_string):
        self.inputwin.clear()
        self.inputwin.addstr(0,0,prompt_string)
        input = self.inputwin.getstr(0,len(prompt_string),60)
        self.inputwin.refresh()
        return input

    def __get_adv_input(self, prompt_string):
        self.inputwin.keypad(1)
        input = array('c')
        histloc = -1
        self.inputwin.clear()
        self.inputwin.addstr(0,0,prompt_string)

        while True:
            i = self.inputwin.getch(0, len(prompt_string) + len(input))
            if i == curses.KEY_ENTER or i == 10:
                break
            elif i == curses.KEY_UP:
                if len(self.history) == 0:
                    self.addToOutput("No Command History yet.")
                elif histloc < len(self.history) - 1:
                    histloc = histloc + 1
                    self.__update_input(''.join([prompt_string, self.history[histloc]]))
                    input = array('c')
                    input.fromstring(self.history[histloc])
            elif i == curses.KEY_DOWN:
                if histloc > 0:
                    histloc = histloc - 1
                    self.__update_input(''.join([prompt_string, self.history[histloc]]))
                    input = array('c')
                    input.fromstring(self.history[histloc])
                else:
                    self.__update_input(prompt_string)
                    input = array('c')
                    histloc = -1
            elif i == curses.KEY_BACKSPACE:
                if len(input) > 0:
                    input.pop()
                    self.inputwin.delch(0,len(input)+1)
            else:
                try:
                    input.append(chr(i))
                except ValueError as ex:
                    self.addToOutput("Key entry error.")

        return input.tostring()

    def __update_input(self, dispStr):
        self.inputwin.clear()
        self.inputwin.addstr(0,0,dispStr)
        self.inputwin.refresh()

    def __update_display(self):
        self.outputwin.clear()
        while self.outputbuffer.count("\n") >= self.yx[0]-1:
            self.outputbuffer.pop(0)
        
        self.outputwin.addstr(0,0,self.outputbuffer.tostring())
        self.outputwin.refresh()

    def addToOutput(self, outstr):
        self.outputbuffer.fromstring(outstr)
        self.outputbuffer.fromstring("\n")
        self.__update_display()

    def run(self):
        self.addToOutput(self.getWelcome())
        line = ''
        while line != EXIT:
            try:
                if len(line) > 0:
                    self.execute(line)

                line = self.__get_adv_input(">")
                self.history.appendleft(line)
            except Exception as ex:
                self.addToOutput("Error Occured:\n")
                self.addToOutput(traceback.format_exc())
                line = ''

        curses.endwin()

    def send(self, packet):
        self.addToOutput(repr(packet[STATUS]))


if __name__ == '__main__':
    try:
        CP = CursesPrompt()
        CP.run()
    except Exception as ex:
        curses.endwin()
        tb = traceback.format_exc()
        print "Catastrophic Error:\n"
        print tb
