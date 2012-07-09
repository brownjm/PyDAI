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

"""Classes and function associated with handling log files for PyDAI."""

import logging
import atexit
from constants import LOGFILE

class Logger(object):
    """Main class to log information from PyDAI that uses a simplified interface to the logging module."""
    def __init__(self, logfilename=LOGFILE, level=3):
        self.logfile = logfilename
        self.running = False
        self.divider = "-"*79 + "\n" # divider between logging sessions

        # setup logging
        logging.basicConfig(filename=self.logfile, format="%(asctime)s %(levelname)-8s%(message)s", level=logging.DEBUG)
        self.level = level
        self._start()
        self.setLevel(level)

    def _start(self):
        """Manually start the logger"""
        if not self.running:
            self.running = True
            self.write(self.divider)
            logging.info("Start logging")
            # register the stop method to be called upon exit of
            # the Python interpreter
            atexit.register(self._stop)

            
    def _stop(self):
        """Manually stop the logger. The stop method has been registered with the atexit module, so it will automatically be called when the Python interpreter is shutting down."""
        if self.running:
            self.info("End logging")
            self.write(self.divider)
            self.running = False

    def setLevel(self, level):
        """Set the level of logging verbosity.
        1 -> log errors only
        2 -> log warnings and errors
        3 -> log everything"""
        if 1 <= level <= 3:
            self.level = 3 # hack for printing following line
            self.info("Logging level set to {}".format(level))
            self.level = level # now set the actual level


    def info(self, infoMessage):
        """Place an information entry into the log file"""
        if self.running and self.level == 3:
            logging.info(infoMessage)

    def warning(self, warningMessage):
        """Place a warning entry into the log file"""
        if self.running and self.level >= 2:
            logging.warning(warningMessage)

    def error(self, errorMessage):
        """Place a warning entry into the log file"""
        if self.running and self.level >= 1:
            logging.error(errorMessage)

    def write(self, text):
        """Write text to the log file"""
        with open(self.logfile, 'a') as f:
            f.write(text)


if __name__ == '__main__':
    log = Logger()
    log.info("Here is some great information")
    log.warning("Something might not be correct")
    log.error("It broke")
