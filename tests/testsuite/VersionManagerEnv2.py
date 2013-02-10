import os, unittest

from java_config_2.VersionManager import VersionManager
from java_config_2.EnvironmentManager import EnvironmentManager

class TestVersionManagerEnv2(unittest.TestCase):

    def setUp(self):
        self.em = EnvironmentManager(os.path.join(os.path.dirname(__file__), 'test_env2'))
        self.em.set_active_vm(self.em.find_vm('icedtea-bin-6'))
        self.verman = VersionManager(self.em)

    def test_get_vm(self):
        vm = self.verman.get_vm("virtual/jdk:1.6 java-virtuals/jdk-with-com-sun dev-java/ant-contrib:0 app-arch/xz-utils >=dev-java/java-config-2.1.9-r1 source? ( app-arch/zip ) >=dev-java/ant-core-1.7.0 dev-java/ant-nodeps >=dev-java/javatoolkit-0.3.0-r2 >=dev-lang/python-2.4")
        self.assertEqual(vm.name(), 'icedtea-bin-6')

if __name__ == '__main__':
    unittest.main()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
