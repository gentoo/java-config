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
        self.providing_packages = ""
        self.providing_vms = ""

        # Arrays of packages/vms as strings, used to delay
        # using of real objects until EnvironmentManager
        # has loaded them all.
        self._packages = []
        self._vms = []

        self.active_package = None
        self.avaliable_vms = []
        
        #self.needs_jdk = False
        self.min_target = None
        #self.min_vm_target = None
        self.loaded = False

        if self._file:
            self._config = EnvFileParser(file).get_config()
            if self._config.has_key("PROVIDERS"):
                self.providing_packages = self._config["PROVIDERS"].replace(" ", ", ")
                temp_packages = self._config["PROVIDERS"].split(' ')
            else:
            	temp_packages = []
            if self._config.has_key("VM"):
                self.providing_vms = self._config["VM"].replace(" ", ", ")
                load_vms = self._config["VM"].split(' ')
            else:
                load_vms = []
        else:
            self._config = {}
            temp_packages = []
        
        # Refactored to make __init__ smaller.
        self.load_providers(temp_packages, load_vms)

    def load_providers(self, temp_packages, vms):
        # Now load system pref.  Really should support
        # List of packages instead of single package.
        

        #ignore preferences until Ive got this working

        #all_prefs = self._manager.get_virtuals_pref().get_config()
        #if all_prefs.has_key(self.name()):
        #    if all_prefs[self.name()] in temp_packages:
        #        self._packages.append(all_prefs[self.name()])
        #else:
        #    if all_prefs.has_key('PREFER_UPSTREAM'):
        #        for package in temp_packages:
        #            if re.compile(all_prefs['PREFER_UPSTREAM'] + '*').match(package):
        #                self._packages.append(package)
        #                break

        for element in temp_packages:
            if not element in self._packages:
                self._packages.append(element)

        for vm in vms:
            if self._manager.get_vm(vm):
                self._vms.append(vm)

    def file(self):
        # Investigate if anything uses this
        # and whether what it should therefore return.
        return self._file

    def description(self):
        try:
            return self.get_provider().description()
        except AttributeError:
            return self._name + ", Using: " + self._manager.get_active_vm().name()

    def get_packages(self):
        return self._packages

    def get_vms(self):
        return self._vms

    def get_available_vms(self):
        return self.available_vms

    def target(self):
        """
        Returns this virtual's target.
        """
        if self.min_target:
            return self.min_target
        #Big Big Hack
        return "1.4"
        #try:
        #    return self.get_provider().query("TARGET")
        #except EnvironmentUndefinedError:
        #    return self.get_provider().query("PROVIDES_VERSION")
            

    def classpath(self):
        """
        Returns this package's classpath
        """
        try:
            return self.get_provider().classpath()
        except AttributeError:
            if self._config.has_key("VM_CLASSPATH"):
                if self._manager.get_active_vm():
                    return self._manager.get_active_vm().query('JAVA_HOME') + self._config["VM_CLASSPATH"]
                else:
                    raise ProviderUnavailableError( self._name, self_providing_vms, self._providing_packages )
            return ""

    def query(self, var):
        """
        Return the value of the requested var from the env file
        """
        if not self.loaded:
            self.load()
        if var == "CLASSPATH":
            return self.classpath()
        if var == "TARGET":
            return self.min_target
        try:
            return self.get_provider().query(var)
        #except EnvironmentUndefinedError:
        except:
            return self._config["VM"]
        #TODO evaluate this!
        #if (var == "TARGET"):
        #    if self.loaded:
        #        return self.min_target, self.needs_jdk
        #    else:
        #        self.load()
        #        return self.min_target, self.needs_jdk
        # 
        #if( var == "CLASSPATH" ):
        #    return self.classpath()
        #
        return ""

    def deps(self):
        """
        Return all packages this package depends on
        """
        try:
            return self.get_provider().deps()
        except:
            return []

    def opt_deps(self):
        """
        Return all packages this package optionally depends on
        """
        try:
            return self.get_provider().opt_deps()
        except:
            return []

    def get_provides(self):
        """
        Return the virtuals this package provides
        """
        return self.get_provider().get_provides()

    #def needs_vm(self):
    #    """
    #    Return whether this Virtual requires a Virtual Machine.
    #    """
    #    return not self.use_active_package()

    def get_provider(self):
        """
        Return whether a package is to be used by the Virtual.
        """
        if not self.loaded:
            self.load()

        if not self._vms and not self.active_package:
            raise ProviderUnavailableError( self._name, self.providing_vms, self.providing_packages ) 

        # If no vm's then use active_package
        if not self._vms and self.active_package:
            return self.active_package

        if self._vms:
            vm = self._manager.get_active_vm()
            try:
                if self._vms.index(vm.name()):
                    # This is acceptable so return false
                    return vm
            except ValueError:
                if not self.active_package:
                    available = ""
                    for vm in self._vms:
                        available = vm + "\n"
                        raise ProviderUnavailableError( self._name, self.providing_vms, self.providing_packages )
        return self.active_package

    def load(self):
        # Active package is the first available package
        for package in self._packages:
            try:
                self.active_package = self._manager.get_package(package)
                self.min_target = self.active_package.query("TARGET")
                break
            except:
                continue

        if self._config.has_key("VM") and self._config["VM"]:
            for vm in self._vms:
                if self._manager.get_vm(vm):
                    avm = self._manager.get_vm(vm)
                    self.avaliable_vms.append( avm )
                    #if self.min_target:
                    #    if cmp(avm.version(), self.min_target) < 0:
                    #        self.min_target = avm.version()
                    #else:
                    #    self.min_target = avm.version()
        #Set loaded to true, so functions can determine what is going on
        self.loaded = True

#vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
