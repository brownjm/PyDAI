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

import router
import device
from constants import SEND, DELETE, EXEC, STATUS, TIMEOUT, ERROR, ROUTER
from constants import QUERY, NAME, MODEL, SN, RETURN, TYPE

class SimulatedDevice(device.Device):
    def __init__(self, attributeDict, commandDict={}):
        device.Device.__init__(self, attributeDict, commandDict)

class Dev1(SimulatedDevice):
    def __init__(self, attributeDict, commandDict={}):
        SimulatedDevice.__init__(self, attributeDict, commandDict)
        self.protocol.backend.funcCallbacks["testFunc"] = self.testFunc

    def testFunc(self):
        return "This is a test"

class AutoDevice(SimulatedDevice):
    def __init__(self, attributeDict, commandDict={}):
        SimulatedDevice.__init__(self, attributeDict, commandDict)
