import unittest
import argparse
from test import parseTest
from src.shell import CursesPrompt


def createSuite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(parseTest))
    return suite

def runTests():
    runner = unittest.TextTestRunner()
    runner.run(createSuite())

def commandLine():
    cp = CursesPrompt()
    cp.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", default=False,
                        help="Run the unit tests")
    args = parser.parse_args()
    
    if args.test == True:
        runTests()
    else:
        commandLine()
