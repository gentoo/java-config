import unittest
from java_config_2.VM import VM
import os

class TestVM(unittest.TestCase):
	path = os.path.join(os.path.dirname(__file__), 'vm_configs')

	def load_vm(self, vm):
		config = os.path.join(self.path,vm)
		return VM(config)

	def setUp(self):
		self.ibm = self.load_vm('ibm-jdk-bin-1.5')
		self.black = self.load_vm('blackdown-jdk-1.4.2')

	def test_empty_provide(self):
		self.failIf(self.ibm.provides("foobar"))
	
	def test_name(self):
		self.assertEqual(self.ibm.name(), 'ibm-jdk-bin-1.5')

	def test_is_build_only(self):
		self.assertTrue(self.black.is_build_only())
		self.assertFalse(self.ibm.is_build_only())

if __name__ == '__main__':
	unittest.main()

