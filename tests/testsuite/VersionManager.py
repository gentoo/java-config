import os, unittest

from java_config_2.VersionManager import VersionManager
from java_config_2.EnvironmentManager import EnvironmentManager

class TestVersionManager(unittest.TestCase):

    def setUp(self):
        self.em = EnvironmentManager(os.path.join(os.path.dirname(__file__), 'test_env'))
        self.em.set_active_vm(self.em.find_vm('ibm-jdk-bin-1.5'))
        self.verman = VersionManager(self.em)

        self.example_dep_vanilla = ">=virtual/jdk-1.5* dev-java/ant-core java-virtuals/jaf"
        self.example_dep_or = "|| ( =virtual/jdk-1.5 =virtual/jdk-1.4 ) dev-java/ant-core java-virtuals/jaf"
        self.example_dep_use = "java? ( >=virtual/jdk-1.5* ) dev-java/ant-core java-virtuals/jaf"

        self.example_slot_dep_vanilla = "virtual/jdk:1.5 dev-java/ant-core:0 java-virtuals/jaf:0"
        self.example_slot_dep_or = "|| ( virtual/jdk:1.4 virtual/jdk:1.4 ) dev-java/ant-core:0 java-virtual/jaf:0"
        self.example_slot_dep_use = "java? ( virtual/jdk:1.5 ) dev-java/ant-core:0 java-virtuals/jaf:0"

    def test_get_vm(self):
        vm = self.verman.get_vm(">=virtual/jdk-1.5* java-virtuals/jaf")
        self.assertEqual(vm.name(), 'sun-jdk-1.6')

        vm = self.verman.get_vm(">=virtual/jdk-1.5* java-virtuals/jaf:0")
        self.assertEqual(vm.name(), 'sun-jdk-1.6')

        vm = self.verman.get_vm("virtual/jdk:1.5")
        self.assertEqual(vm.name(), 'ibm-jdk-bin-1.5')

        self.assertRaises(Exception, self.verman.get_vm, 'virtual/jdk:1.4')
        self.assertRaises(Exception, self.verman.get_vm, '=virtual/jdk-1.4*', False)

        vm = self.verman.get_vm('virtual/jdk:1.4', True)
        self.assertTrue(vm.name(), 'blackdown-jdk-1.4.2')

        self.assertRaises(Exception, self.verman.get_vm, 'virtual/jdk:1.4 dev-java/test-package:0')

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
        vm = self.em.get_vm('sun-jdk-1.6')
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
        self.assertFalse(self.verman.version_satisfies('java6? ( =virtual/jdk-1.6 ) !java6? ( =virtual/jdk-1.5 )', vm))

    #def test_parse_depend(self):

    #def test_get_prefs(self):

    #def test_parse_depend_virtuals(self):

    #def test_get_lowest_atom(self):

    def test_get_lowest(self):
        target = self.verman.get_lowest(">=virtual/jdk-1.4")
        self.assertEquals(target, '1.4')
        
        target = self.verman.get_lowest(self.example_dep_vanilla)
        self.assertEquals(target, '1.5')

        target = self.verman.get_lowest(self.example_dep_or)
        self.assertEquals(target, '1.4')
        
    def test_get_lowest_with_package_dep(self):
        pass
        # 1.4 dep but ant-cores5 has a 1.8 target.
        #self.assertRaises(Exception, self.verman.get_lowest, 'virtual/jdk:1.4 dev-java/test-package:0')
        # 1.4 but has a 1.5 target package.
        #self.assertRaises(Exception, self.verman.get_lowest, '>=virtual/jdk-1.4 dev-java/ant-cores5:0')

    #def test_find_vm(self):

    #def test_matches(self):

    def test_version_cmp(self):
        self.assertEquals(self.verman.version_cmp('1.5.2', '1.5.2'), 0)
        self.assertTrue(self.verman.version_cmp('1.5', '1.5.1') < 0)
        self.assertTrue(self.verman.version_cmp('1.5.1', '1.5') > 0)

    #def test_matches(self):

if __name__ == '__main__':
    unittest.main()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
