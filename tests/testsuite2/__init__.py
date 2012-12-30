__all__ = [ 'VersionManager' ]
from . import VersionManager
import os
from java_config_2.EnvironmentManager import EnvironmentManager as em
em.vms_path = os.path.join(os.path.dirname(__file__), 'vm_configs')
em.pkg_path = path = os.path.join(os.path.dirname(__file__), 'packages', '%s/package.env')
em.virtual_path = os.path.join(os.path.dirname(__file__), 'virtual_configs') + '/'
em.set_active_vm(em.find_vm('icedtea-bin-7')[0])

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
