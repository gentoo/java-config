import unittest
from java_config_2.Virtual import Virtual
from java_config_2.EnvironmentManager import EnvironmentManager as em
import os

class TestVirtual(unittest.TestCase):
	def load_virtual(self, virtual):
		dir = os.path.dirname(__file__)
		config = os.path.join(dir,'virtual_configs',virtual)
		return Virtual(virtual, em, config)

	def setUp(self):
		self.jaf = self.load_virtual('jaf')

	def test_get_vms(self):
		self.assertEqual(self.jaf.get_vms(), ['sun-jdk-1.6'])
	
if __name__ == '__main__':
	unittest.main()

