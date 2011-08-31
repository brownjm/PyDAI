"""Module to provide simple methods of managing devices based on configuration 
files found in devices folder."""

import os
import shutil
import device

class DeviceFactory(object):
    """Provides methods to produce Device classes from configuration files."""
    def __init__(self, devicefolder):
        self.dir = devicefolder

    def genConfigTemplate(self, filename):
        """Generate a blank configuration file allowing users to add in 
specific values of their device."""
        shutil.copy("devicetemplate", os.path.join(self.dir, filename))

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

if __name__ == "__main__":
    df = DeviceFactory("devices")
    df.genConfigTemplate("dev1")
