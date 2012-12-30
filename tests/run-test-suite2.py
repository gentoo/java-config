import unittest as u
import testsuite2
import sys

suite = u.defaultTestLoader.loadTestsFromNames(testsuite2.__all__, testsuite2)

result = u.TextTestRunner().run(suite)
sys.exit(not result.wasSuccessful())
