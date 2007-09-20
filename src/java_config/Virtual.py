# -*- coding: UTF-8 -*-

# Copyright 2004-2007 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from FileParser import *
from Package import *
import re, sys
        
class Virtual(Package):
    """
    Class representing an installed java virtual.
    """
    def __init__(self, name, manager, file = None):
        self._file = file
        self._name = name
        self._manager = manager

        # Store possible installed packages and vms in arrays
        self._packages = []
        self._vms = []
        self.active_package = None
        self.needs_jdk = False
        self.min_target = None
        self.min_vm_target = None
        self.loaded = False

        if self._file:
            self._config = EnvFileParser(file).get_config()
            temp_packages = self._config["PROVIDERS"].split(' ')
        else:
            self._config = {}
            temp_packages = []
        
        # Refactored to make __init__ smaller.
        self.load_providers(temp_packages)

    def load_providers(self, temp_packages):
        # Now load system pref.  Really should support
        # List of packages instead of single package.
        all_prefs = self._manager.get_virtuals_pref().get_config()
        if all_prefs.has_key(self.name()):
            if all_prefs[self.name()] in temp_packages:
                self._packages.append(all_prefs[self.name()])
        else:
            if all_prefs.has_key('PREFER_UPSTREAM'):
                for package in temp_packages:
                    if re.compile(all_prefs['PREFER_UPSTREAM'] + '*').match(package):
                        self._package.append(package)
                        break

        for element in temp_packages:
            if not element in self._packages:
                self._packages.append(element)

    def file(self):
        # Investigate if anything uses this
        # and whether what it should therefore return.
        return self._file

    def description(self):
        if not self.use_active_package():
            return self._name + ", Using: " + self._manager.get_active_vm().name()
        return self.get_active_package().description()

    def get_packages(self):
        return self._packages

    def classpath(self):
        """
        Returns this package's classpath
        """
        if not self.use_active_package():
            return self._manager.get_active_vm().query('JAVA_HOME') + self._config["VM_CLASSPATH"]
        return self.get_active_package().classpath()

    def query(self, var):
        """
        Return the value of the requested var from the env file
        """
        if (var == "TARGET"):
            if self.loaded:
                return self.min_target, self.needs_jdk
            else:
                self.load()
                return self.min_target, self.needs_jdk
        
        if( var == "CLASSPATH" ):
            return self.classpath()
        
        return ""

    def deps(self):
        """
        Return all packages this package depends on
        """
        if not self.use_active_package():
            return []
        return self.get_active_package().deps()

    def opt_deps(self):
        """
        Return all packages this package optionally depends on
        """
        if not self.use_active_package():
            return []
        return self.get_active_package().opt_deps()

    def provides(self):
        """
        Return the virtuals this package provides
        """
        if not self.use_active_package():
            return self._manager.get_active_vm().provides()
        return self.get_active_package().provides()

    def get_active_package(self):
        if not self.loaded:
            self.load()
        return self.active_package

    def use_active_package(self):
        #Check whether load function has been called.
        if not self.loaded:
            self.load()

        if not self._vms and not self.active_package:
            raise Exception("Couldn't find suitable package or vm to provide: " + self._name)

        # If no vm's then use active_package
        if not self._vms and self.active_package:
            #return self.active_package
            return True

        if self._vms:
            import VersionManager
            verman = VersionManager.VersionManager()
            vm = self._manager.get_active_vm()
            if verman.version_satisfies( self._config["VM"], vm ):
                # This is an acceptable so return false
                return False
            else:
                if not self.active_package:
                    available = ""
                    for vm in self._vms:
                        available = vm.name() + "\n"
                    print "Please use one of the following vm's"
                    print available
                else:
                    return True

    def load(self):
        # Active package is the first available package
        for package in self._packages:
            # Improvement: we could put the VM in the list of providers
            if self._manager.get_package(package) is not None:
                self.active_package = self._manager.get_package(package)
        # Set the minimum target version to the active package's target.
        if self.active_package:
            self.min_target = self.active_package.query("TARGET")

        # Load possible vms.  These are vm's that are installed.
        vms = self._manager.get_virtual_machines()

        if self._config["VM"]:
            import VersionManager
            verman = VersionManager.VersionManager()

            # We assume that there was only one virtual/[jre|jdk] declared.
            r = verman.parse_depend(self._config["VM"])[0]
            version = r["version"]
            if r["type"] == "jdk":
                self.needs_jdk = True

            for vm_index in vms:
                vm = vms[vm_index]
                if self.needs_jdk and not vm.is_jre:
                    continue
                if verman.version_satisfies( self._config["VM"], vm ):
                    self._vms.append(vm)
                    if self.min_target:
                        if cmp(vm.version(), self.min_target) < 0:
                            self.min_target = vm.version()
                    else:
                        self.min_target = vm.version()
                    if self.min_vm_target:
                        if cmp(vm.version(), self.min_vm_target) < 0:
                            self.min_vm_target = vm.version()
                    else:
                        self.min_vm_target = vm.version()

        #Set loaded to true, so function can determine what is going on
        self.loaded = True

#vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
