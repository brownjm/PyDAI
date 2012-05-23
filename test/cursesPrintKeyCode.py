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

import curses
stdscr = curses.initscr()

begin_x = 20 ; begin_y = 7
height = 5 ; width = 40

try:
    win = curses.newwin(height, width, begin_y, begin_x)
    i = stdscr.getch(0, 10)
    curses.echo()
#win.addstr(i)
    #stdscr.refresh()
except:
    pass
finally:
    curses.endwin()
