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

"""Module to provide simple methods of managing devices based on configuration 
files found in devices folder."""

import device

class DeviceFactory(object):
    """Provides methods to produce Device classes from configuration files."""
    def __init__(self, devicefolder):
        self.dir = devicefolder

    def genConfigTemplate(self):
        """Generate a blank configuration file allowing users to add in 
specific values of their device."""
        pass

    def constructDevice(self, filename):
        """Read in device from string and construct a Device object"""
        pass


# define exceptions
class FileNotFoundError(Exception):
    def __init__(self, filename):
        self.msg = "Could not locate configuration file: {0}".format(filename)
    def __str__(self):
        return self.msg

class ConfigFileError(Exception):
    def __init__(self, filename):
        self.msg = "Malformed configuration file: {0}".format(filename)
    def __str__(self):
        return self.msg
