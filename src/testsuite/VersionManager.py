import unittest
from java_config_2.VersionManager import VersionManager


class TestVersionManager(unittest.TestCase):
	verman = VersionManager()

	def test_get_vm(self):
		vm = self.verman.get_vm(">=virtual/jdk-1.5 java-virtuals/jaf")
		self.assertEqual(vm.name(), 'sun-jdk-1.6')
	
if __name__ == '__main__':
	unittest.main()

