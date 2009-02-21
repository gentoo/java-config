import unittest
import os

class TestPackage(unittest.TestCase):
	path = os.path.join(os.path.dirname(__file__), 'packages', '%s/package.env')

if __name__ == '__main__':
	unittest.main()
