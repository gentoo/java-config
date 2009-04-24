import unittest
import os
from java_config_2.VersionManager import VersionManager
from java_config_2.EnvironmentManager import EnvironmentManager as em

class TestVersionManager(unittest.TestCase):
	verman = VersionManager()

	def setUp(self):
		self.example_dep_vanilla = ">=virtual/jdk-1.5* dev-java/ant-core java-virtuals/jaf"
		self.example_dep_or = "|| ( =virtual/jdk-1.5 =virtual/jdk-1.4 ) dev-java/ant-core java-virtuals/jaf"
		self.example_dep_use = "java? ( >=virtual/jdk-1.5* ) dev-java/ant-core java-virtuals/jaf"

		self.example_slot_dep_vanilla = "virtual/jdk:1.5 dev-java/ant-core:0 java-virtuals/jaf:0"
		self.example_slot_dep_or = "|| ( virtual/jdk:1.4 virtual/jdk:1.4 ) dev-java/ant-core:0 java-virtual/jaf:0"
		self.example_slot_dep_use = "java? ( virtual/jdk:1.5 ) dev-java/ant-core:0 java-virtuals/jaf:0"

	def test_get_vm(self):
		vm = self.verman.get_vm(">=virtual/jdk-1.5* java-virtuals/jaf")
		self.assertEqual(vm.name(), 'sun-jdk-1.6')

		vm = self.verman.get_vm("virtual/jdk:1.5")
		self.assertEqual(vm.name(), 'ibm-jdk-bin-1.5')

	def test_filter_depend_vanilla(self):
		os.environ["USE"] = ""
		self.assertEquals(self.verman.filter_depend(self.example_dep_vanilla), self.example_dep_vanilla)

	def test_filter_depend_or(self):
		# Oh you only realise how ugly things are once you write unittests.
		os.environ["USE"] = ""
		rmatch = "|| =virtual/jdk-1.5 =virtual/jdk-1.4 dev-java/ant-core java-virtuals/jaf"
		self.assertEquals(self.verman.filter_depend(self.example_dep_or), rmatch)
	
	def test_filter_depend_use(self):
		os.environ["USE"] = "java"
		rmatch = ">=virtual/jdk-1.5* dev-java/ant-core java-virtuals/jaf"
		self.assertEquals(self.verman.filter_depend(self.example_dep_use), rmatch)

	def test_version_satisfies(self):
		vm = em.get_vm('sun-jdk-1.6')
		self.assertTrue(self.verman.version_satisfies('>=virtual/jdk-1.5', vm))
		self.assertFalse(self.verman.version_satisfies('>=virtual/jdk-1.7', vm))
		self.assertTrue(self.verman.version_satisfies('|| ( =virtual/jdk-1.6 =virtual/jdk-1.5 )', vm))

		self.assertTrue(self.verman.version_satisfies('virtual/jdk:1.6', vm))
		self.assertFalse(self.verman.version_satisfies('virtual/jdk:1.5', vm))
		self.assertTrue(self.verman.version_satisfies('>=virtual/jdk-1.5', vm))

		#this will be interesting from the perspective of environment handling.

		os.environ["USE"] = "java6"
		self.assertTrue(self.verman.version_satisfies('java6? ( =virtual/jdk-1.6 )', vm))
		os.environ["USE"] = ""
		self.assertFalse(self.verman.version_satisfies('java6? ( =virtual/jdk-1.6) !java6? ( =virtual/jdk-1.5 )', vm))

	def test_parse_depend(self):
		"""
		
		"""


	#def test_get_prefs(self):

	#def test_parse_depend_virtuals(self):

	#def test_get_lowest_atom(self):

	#def test_get_lowest(self):

	#def test_find_vm(self):

	#def test_matches(self):

	def test_version_cmp(self):
		self.assertEquals(self.verman.version_cmp('1.5.2', '1.5.2'), 0)
		self.assertTrue(self.verman.version_cmp('1.5', '1.5.1') < 0)
		self.assertTrue(self.verman.version_cmp('1.5.1', '1.5') > 0)

	#def test_matches(self):

if __name__ == '__main__':
	unittest.main()

