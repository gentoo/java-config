__all__ = [ 'VM', 'Virtual', 'VersionManager' ]
import VM
import Virtual
import VersionManager
from java_config_2.EnvironmentManager import EnvironmentManager as em
em.vms_path = VM.TestVM.path
em.set_active_vm(em.find_vm('ibm-jdk-bin-1.5'))
