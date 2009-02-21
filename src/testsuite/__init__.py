__all__ = [ 'VM', 'Virtual', 'Package', 'VersionManager', 'EnvironmentManager' ]
import VM
import Virtual
import Package
import VersionManager
import EnvironmentManager
from java_config_2.EnvironmentManager import EnvironmentManager as em
em.vms_path = VM.TestVM.path
em.pkg_path = Package.TestPackage.path
em.virtual_path = Virtual.TestVirtual.path
em.set_active_vm(em.find_vm('ibm-jdk-bin-1.5'))
