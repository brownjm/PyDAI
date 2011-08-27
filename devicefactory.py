"""Module to provide simple methods of managing devices based on configuration 
files found in devices folder."""

class DeviceFactory(object):
    """Provides methods to produce Device classes from configuration files."""
    pass


# define exceptions
class FileNotFoundError(Exception):
    def __init__(self, string):
        self.msg = "Could not locate configuration file: {0}".format(string)
    def __str__(self):
        return self.msg

class ConfigFileError(Exception):
    def __init__(self, string):
        self.msg = "Malformed configuration file: {0}".format(string)
    def __str__(self):
        return self.msg
