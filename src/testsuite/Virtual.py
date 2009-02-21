import unittest
from java_config_2.Virtual import Virtual
from java_config_2.EnvironmentManager import EnvironmentManager as em
import os

class TestVirtual(unittest.TestCase):
	path = os.path.join(os.path.dirname(__file__), "virtual_configs") + "/"

	def load_virtual(self, virtual):
		config = os.path.join(TestVirtual.path,virtual)
		return Virtual(virtual, em, config)

	def setUp(self):
		self.jaf = self.load_virtual('jaf')
		self.jdbc = self.load_virtual('jdbc')

	def test_get_vms(self):
		self.assertEqual(self.jaf.get_vms(), ['sun-jdk-1.6'])
	
if __name__ == '__main__':
	unittest.main()

