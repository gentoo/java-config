import unittest
from java_config_2 import EnvironmentManager
em = EnvironmentManager.EnvironmentManager()

class TestOldProvides(unittest.TestCase):
	def testprovide(self):
		vm = em.find_vm("ibm-jdk-bin-1.5")[0]
		self.assert_(vm, "You need to install ibm-jdk-bin:1.5 for the tests")
		self.failIf(vm.provides("foobar"))

if __name__ == '__main__':
	unittest.main()
