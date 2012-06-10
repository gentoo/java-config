import unittest
import os
from java_config_2.VersionManager import VersionManager
from java_config_2.EnvironmentManager import EnvironmentManager as em

class TestVersionManager(unittest.TestCase):
    verman = VersionManager()

    def test_get_vm(self):
        vm = self.verman.get_vm("virtual/jdk:1.6 java-virtuals/jdk-with-com-sun dev-java/ant-contrib:0 app-arch/xz-utils >=dev-java/java-config-2.1.9-r1 source? ( app-arch/zip ) >=dev-java/ant-core-1.7.0 dev-java/ant-nodeps >=dev-java/javatoolkit-0.3.0-r2 >=dev-lang/python-2.4")
        self.assertEqual(vm.name(), 'icedtea-bin-6')

if __name__ == '__main__':
    unittest.main()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
