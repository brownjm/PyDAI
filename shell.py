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

class CommandLinePrompt(Executable):
    def run(self):
        self.doWelcome()
        while 1:
            try:
                line = raw_input('> ')
                if line == EXIT:
                    break
                if len(line) > 0:
                    self.execute(line)

            except Exception as ex:
                print ex

    def send(self, packet):
        print packet[STATUS]


if __name__ == '__main__':
    CLP = CommandLinePrompt()
    CLP.run()
