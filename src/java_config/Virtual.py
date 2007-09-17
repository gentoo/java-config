# -*- coding: UTF-8 -*-

# Copyright 2004-2007 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from FileParser import *
from Package import *
import re, sys
#from java_config.VersionManager import *
#import VersionManager
        
class Virtual(Package):
    """
    Class representing an installed java virtual.
    """
    def __init__(self, name, manager, file = None):
        self._file = file
        self._name = name
        self._manager = manager
        self._packages = []
        self.active_package = None
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
        all_prefs = self._manager.get_virtual_pref().get_config()
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
        return self.get_active_package().description()

    def get_packages(self):
        return self._packages

    def classpath(self):
        """
        Returns this package's classpath
        """
        if self.get_active_package() == "VM":
            return self._manager.get_active_vm().query('JAVA_HOME') + self._config["VM_CLASSPATH"]
        return self.get_active_package().classpath()

    def query(self, var):
        """
        Return the value of the requested var from the env file
        """
        active_package = self.get_active_package()
        
        if active_package == "VM":
            if (var == "TARGET"):
                import VersionManager
                verman = VersionManager.VersionManager()
                r = verman.parse_depend(self._config["VM"])[0]
                version = r["version"]
                if r["type"] == "jdk":
                    needs_jdk = True
                else:
                    needs_jdk = False
                return version, needs_jdk
            if (var == "CLASSPATH"):
                return self._manager.get_active_vm().query('JAVA_HOME') + self._config["VM_CLASSPATH"]
            return ""
        
        else:
            return active_package.query(var)

    def deps(self):
        """
        Return all packages this package depends on
        """
        if self.get_active_package() == "VM":
            return []
        return self.get_active_package().deps()

    def opt_deps(self):
        """
        Return all packages this package optionally depends on
        """
        if self.get_active_package() == "VM":
            return []
        return self.get_active_package().opt_deps()

    def provides(self):
        """
        Return the virtuals this package provides
        """
        return self.get_active_package().provides()

    def get_active_package(self):
        if not self.active_package:
            self.load_active_package()
        return self.active_package

    def load_active_package(self):      
        # Must obtain the VersionManager, this is ugly but avoids circular dependencies...
        import VersionManager
        verman = VersionManager.VersionManager()
        if (verman.version_satisfies(self._config["VM"], self._manager.get_active_vm())):
            # We should return the special string "VM"
            self.active_package = "VM"
            return
        # Active package is the first available package.
        
        for package in self._packages:
            # Improvement: we could put the VM in the list of providers 
            
            if self._manager.get_package(package) is not None:
                self.active_package = self._manager.get_package(package)
                return
        if self._config["VM"]:
            self.active_package = "VM"
            return          
            
        if not self.active_package:
            #Eventually this should throw an error?
            raise Exception("Couldn't find package providing virtual " + self._name)
            #self.active_package = Package("No package provided.")


#vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
