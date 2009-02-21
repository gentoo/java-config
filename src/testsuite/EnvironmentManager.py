import unittest
import os

from java_config_2.EnvironmentManager import EnvironmentManager as em

class TestEnvironmentManager(unittest.TestCase):
	path=""

	def test_get_package(self):
		em.get_package('ant-cores')

if __name__ == '__main__':
	unittest.main()
