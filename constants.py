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

"""Module to hold program wide constants"""

# Names of files and directories
DEVFOLDER = "devices"
DEVTEMPLATE = "devicetemplate"

# Names of devices
DEVMAN = "devman"       # device manager
EXEC = "exec"           # executable
ROUTER = "router"       # router

# Commands
NEW = "new"             # create something
DELETE = "delete"       # delete something
GET = "get"             # run command on device
FROM = "from"           # sets destination
QUERY = "query"         # request information
STATUS = "status"       # reponse to user on status of received packet
EXIT = "exit"           # exits program

# Device configuration file constants
NAME = "name"
VENDOR = "vendor"
MODEL = "model"
SN = "sn"
PROTOCOL = "protocol"

# Protocol types
SIMULATED = "simulated"
