import unittest
import os

from java_config_2.EnvironmentManager import EnvironmentManager as em

class TestEnvironmentManager(unittest.TestCase):
    path=""

    def test_load_packages(self):
        em.packages = {}
        em.load_packages()
        self.assertEquals(len(em.packages), 11)

    def test_get_package(self):
        em.get_package('ant-cores')

    def test_build_dep_path(self):
        self.assertTrue( len(em.build_dep_path(["jdbc"], "CLASSPATH", set())) > 2)

if __name__ == '__main__':
    unittest.main()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
