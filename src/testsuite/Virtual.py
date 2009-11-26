import unittest
import os
from java_config_2.Virtual import Virtual
from java_config_2.EnvironmentManager import EnvironmentManager as em
from java_config_2.Errors import ProviderUnavailableError

def load_virtual(virtual):
    config = os.path.join(TestVirtual.path, virtual)
    return Virtual(virtual, em, config)

class TestVirtual(unittest.TestCase):
    path = os.path.join(os.path.dirname(__file__), "virtual_configs") + "/"

    def setUp(self):
        self.jaf = load_virtual('jaf')
        self.jmx = load_virtual('jmx')
        self.jmx2 = load_virtual('jmx2')

    def test_get_vms(self):
        self.assertEqual(self.jaf.get_vms(), ['sun-jdk-1.6'])
    
    def test_load_vms(self):
        self.assertEqual( self.jmx._vms, ['ibm-jdk-bin-1.5', 'sun-jdk-1.6' , \
            'sun-jdk-1.7', 'sun-jre-bin-1.6'] )
        self.assertEqual( self.jmx2._vms, ['ibm-jdk-bin-1.5', 'sun-jdk-1.6' , \
            'sun-jdk-1.7', 'sun-jre-bin-1.6'] )

class TestMultiProviderVirtual(unittest.TestCase):

    def setUp(self):
        em.set_active_vm(em.get_vm('sun-jdk-1.6'))
        self.jdbc = load_virtual('jdbc')
    
    def test_classpath_multiple(self):
        self.assertEqual( len(self.jdbc.classpath().split(':')), 2)

    def test_invalid_vm_error(self):
        em.set_active_vm(em.get_vm('ibm-jdk-bin-1.5'))
        self.assertRaises( ProviderUnavailableError, self.jdbc.classpath )

if __name__ == '__main__':
    unittest.main()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
