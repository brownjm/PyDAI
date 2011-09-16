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
from array import array

class CursesPrompt(Executable):
    def __init__(self):
        Executable.__init__(self)
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
        line = self.__get_input(">")
        while line != EXIT:
            try:
                if len(line) > 0:
                    self.execute(line)
            except Exception as ex:
                self.addToOutput("Error Occured:\n")
                self.addToOutput(traceback.format_exc())
                #raise ex
            finally:
                line = self.__get_input(">")
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
