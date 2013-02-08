import os, unittest

from java_config_2.Virtual import Virtual
from java_config_2.EnvironmentManager import EnvironmentManager
from java_config_2.Errors import ProviderUnavailableError

class TestVirtual(unittest.TestCase):

    def setUp(self):
        em = EnvironmentManager(os.path.join(os.path.dirname(__file__), 'test_env'))
        em.set_active_vm(em.find_vm('ibm-jdk-bin-1.5'))

        self.jaf = em.get_virtual('jaf')
        self.jmx = em.get_virtual('jmx')
        self.jmx2 = em.get_virtual('jmx2')

    def test_get_vms(self):
        self.assertEqual(self.jaf.get_vms(), ['sun-jdk-1.6'])
    
    def test_load_vms(self):
        self.assertEqual( self.jmx._vms, ['ibm-jdk-bin-1.5', 'sun-jdk-1.6' , \
            'sun-jdk-1.7', 'sun-jre-bin-1.6'] )
        self.assertEqual( self.jmx2._vms, ['ibm-jdk-bin-1.5', 'sun-jdk-1.6' , \
            'sun-jdk-1.7', 'sun-jre-bin-1.6'] )

class TestMultiProviderVirtual(unittest.TestCase):

    def setUp(self):
        em = EnvironmentManager(os.path.join(os.path.dirname(__file__), 'test_env'))
        em.set_active_vm(em.get_vm('sun-jdk-1.6'))

        self.jdbc = em.get_virtual('jdbc')
    
    def test_classpath_multiple(self):
        self.assertEqual( len(self.jdbc.classpath().split(':')), 2)

if __name__ == '__main__':
    unittest.main()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
