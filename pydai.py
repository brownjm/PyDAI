import unittest
import argparse
import sys
import os
from test import parserTest
from src.shell import CursesPrompt


def createSuite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(parserTest))
    return suite

def runTests():
    runner = unittest.TextTestRunner()
    runner.run(createSuite())

def commandLine():
    cp = CursesPrompt()
    cp.run()

if __name__ == "__main__":
    os.chdir("src")
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", default=False,
                        help="Run the unit tests")
    args = parser.parse_args()
    
    if args.test == True:
        runTests()
    else:
        commandLine()
