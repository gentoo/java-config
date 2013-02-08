import os, unittest

from java_config_2.EnvironmentManager import EnvironmentManager

class TestEnvironmentManager(unittest.TestCase):

    def setUp(self):
        self.em = EnvironmentManager(os.path.join(os.path.dirname(__file__), 'test_env'))
        self.em.set_active_vm(self.em.find_vm('ibm-jdk-bin-1.5'))

    def test_load_packages(self):
        self.em.packages = {}
        self.em.load_packages()
        self.assertEquals(len(self.em.get_packages()), 11)

    def test_get_package(self):
        self.em.get_package('ant-cores')

    def test_build_dep_path(self):
        self.assertTrue( len(self.em.build_dep_path(["jdbc"], "CLASSPATH", set())) > 2)

if __name__ == '__main__':
    unittest.main()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
