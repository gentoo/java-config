import os, unittest

from java_config_2.EnvironmentManager import EnvironmentManager
from java_config_2.VM import VM

class TestVM(unittest.TestCase):

    def load_vm(self, vm):
        config = os.path.join(self.path,vm)
        return VM(config)

    def setUp(self):
        em = EnvironmentManager(os.path.join(os.path.dirname(__file__), 'test_env'))

        self.ibm = em.get_vm('ibm-jdk-bin-1.5')
        self.black = em.get_vm('blackdown-jdk-1.4.2')

    def test_empty_provide(self):
        self.assertFalse(self.ibm.provides("foobar"))
    
    def test_name(self):
        self.assertEqual(self.ibm.name(), 'ibm-jdk-bin-1.5')

    def test_is_build_only(self):
        self.assertTrue(self.black.is_build_only())
        self.assertFalse(self.ibm.is_build_only())

if __name__ == '__main__':
    unittest.main()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
