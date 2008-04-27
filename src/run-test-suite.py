import unittest as u
import testsuite
import sys

suite = u.defaultTestLoader.loadTestsFromNames(testsuite.__all__, testsuite)

result = u.TextTestRunner().run(suite)
sys.exit(not result.wasSuccessful())
