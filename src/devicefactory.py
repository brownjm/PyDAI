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

import os
import shutil
import device
from constants import DEVFOLDER, DEVTEMPLATE

class DeviceFactory(object):
    """Provides methods to produce Device classes from configuration files."""
    def __init__(self, devicefolder=DEVFOLDER):
        self.dir = devicefolder
        self.devices = []
        self._updateDevList()

    def _updateDevList(self):
        """Updates the list of available devices"""
        filenames = os.listdir(self.dir)
        for dev in filenames:
            if dev not in self.devices:
                self.devices.append(dev)

    def genConfigTemplate(self, filename):
        """Generate a blank configuration file allowing users to add in 
specific values of their device."""
        shutil.copy(DEVTEMPLATE, os.path.join(self.dir, filename))
        self._updateDevList()

    def constructDevice(self, filename):
        """Read in device from string and construct a Device object"""
        fn = os.path.join(self.dir, filename)
        try:
            with open(fn, "r") as f:
                data = f.readlines()
        except IOError:
            raise FileNotFoundError(fn)

        # remove unnecessary lines
        lines = []
        for line in data:
            if not (line.startswith("#") or line.startswith("\n") or 
                    line.startswith("@")):
                lines.append(line.strip("\n"))
        
        # construct the dictionaries
        attributeDict = {}
        commandDict = {}
        entry = []
        self.l = lines
        for line in lines:
            if "=" in line: # must be an attribute
                entry = line.split("=")
                entry = [word.strip() for word in entry] # strip whitespace
                if len(entry) is not 2:
                    raise ConfigFileError(fn, line)
                attributeDict[entry[0]] = entry[1]

            elif "|" in line: # must be a command
                entry = line.split("|")
                entry = [word.strip() for word in entry] # strip whitespace
                if len(entry) is not 3:
                    raise ConfigFileError(fn, line)
                commandDict[entry[0]] = (entry[1], entry[2])
            else:
                raise ConfigFileError(fn, line)

        # create device from newly formed dictionaries
        self.att = attributeDict
        return device.Device(attributeDict, commandDict)


# define exceptions
class FileNotFoundError(Exception):
    def __init__(self, filename):
        self.msg = "Could not locate configuration file: {0}".format(filename)
    def __str__(self):
        return self.msg

class ConfigFileError(Exception):
    def __init__(self, filename, line="Unknown"):
        self.msg = "Malformed configuration file: {0} -> {1}".format(filename, line)
    def __str__(self):
        return self.msg

if __name__ == "__main__":
    df = DeviceFactory()
    dev = df.constructDevice("dev1")
    print dev
    print dev.command
