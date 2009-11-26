import unittest
import os

from java_config_2.Package import Package

class TestPackage(unittest.TestCase):
    path = os.path.join(os.path.dirname(__file__), 'packages', '%s/package.env')

    def load_package(self, package):
        config = TestPackage.path % package
        return Package(package, config)

    def setUp(self):
        self.ant = self.load_package('ant-cores')

    def test_package_info(self):
        #using a package we definitely
        #know will not be into the tree
        #to ensure we ain't using real system packages.
        self.assertEqual(self.ant.name(), 'ant-cores')
        self.assertEqual(self.ant.description(), "Description: %s" % self.ant.name())
        self.assertEqual(self.ant.target(), "1.4")
        self.assertTrue(self.ant.query('JAVADOC_PATH'))
        self.assertFalse(self.ant.query('VAR_SHOULD_NOT_EXIST'))

if __name__ == '__main__':
    unittest.main()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
