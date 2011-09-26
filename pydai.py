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
