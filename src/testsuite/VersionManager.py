import unittest
import os
from java_config_2.VersionManager import VersionManager
from java_config_2.EnvironmentManager import EnvironmentManager as em

class TestVersionManager(unittest.TestCase):
	verman = VersionManager()

	def test_get_vm(self):
		vm = self.verman.get_vm(">=virtual/jdk-1.5 java-virtuals/jaf")
		self.assertEqual(vm.name(), 'sun-jdk-1.6')

	def test_target_matches(self):
		vm = em.get_vm('sun-jdk-1.6')
		self.assertTrue(self.verman.version_satisfies('>=virtual/jdk-1.5', vm))
		self.assertFalse(self.verman.version_satisfies('>=virtual/jdk-1.7', vm))
		self.assertTrue(self.verman.version_satisfies('|| ( =virtual/jdk-1.6 =virtual/jdk-1.5 )', vm))

		#this will be interesting from the perspective of environment handling.

		os.environ["USE"] = "java6"
		self.assertTrue(self.verman.version_satisfies('java6? ( =virtual/jdk-1.6 )', vm))
		os.environ["USE"] = ""
		self.assertFalse(self.verman.version_satisfies('java6? ( =virtual/jdk-1.6) !java6? ( =virtual/jdk-1.5 )', vm))
	
if __name__ == '__main__':
	unittest.main()

