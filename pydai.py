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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", default=False,
                        help="Run the unit tests")
    args = parser.parse_args()
    
    if args.test == True:
        runTests()
    else:
        commandLine()
