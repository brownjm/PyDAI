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

"""Main script to run and test PyDAI. Run in terminal with '-h' option for help
"""

import unittest
import argparse
from test import parseTest
from src.shell import CursesPrompt
from src.router import Router
from src.devicemanager import DeviceManager
from multiprocessing import Event

def createSuite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(parseTest))
    return suite

def runTests():
    runner = unittest.TextTestRunner()
    runner.run(createSuite())

def commandLine():
    devStop = Event()
    routeStop = Event()
    r = Router()
    r.procStop = routeStop
    r.start()
    d = DeviceManager()
    d.procStop = devStop
    d.start()
    cp = CursesPrompt()
    cp.run()
    print "Shutting Down Device Manager..."
    devStop.set()
    d.join()
    print "Done"
    print "Shutting Down Router..."
    routeStop.set()
    r.join()
    print "Done"

def server(address, akey):
    r = Router(address, akey)
    d = DeviceManager(address, akey)
    r.start()
    d.start()
    print "Server is Running..."
    d.join()
    r.join()
    print "Server is Shut Down..."

def client(address, akey):
    cp = CursesPrompt(address, akey)
    cp.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", default=False,
                        help="Run the unit tests")
    parser.add_argument("--server", action="store_true", default=False,
                        help="Run PyDAI as a server")
    parser.add_argument("--client", action="store_true", default=False,
                        help="Run PyDAI as a client connecting to a PyDAI server")
    parser.add_argument("--ip", default='localhost',
                        help="Specifies ip to run on or connect to")
    parser.add_argument("--port", default='15000',
                        help="Specifies port to use when running or connecting")
    parser.add_argument("--authkey", default='12345',
                        help="Authentication key to use when running or connecting")
    args = parser.parse_args()
    
    if args.test == True:
        runTests()
    else:
        if args.server == True:
            server((args.ip, int(args.port)), args.authkey)
        elif args.client == True:
            client((args.ip, int(args.port)), args.authkey)
        else:
            commandLine()
