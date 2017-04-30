# -*- coding: UTF-8 -*-

# Copyright 2004-2013 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $


from java_config_2.FileParser import *
from java_config_2.Errors import EnvironmentUndefinedError, ProviderUnavailableError
from java_config_2.Package import *
from java_config_2.VersionManager import VersionManager
import re, sys


class Virtual(Package):
    """
    Class representing an installed java virtual.
    """
    def __init__(self, name, manager, file = None):
        self._file = file
        self._name = name
        self._manager = manager

        # Arrays of packages/vms as strings, used to delay
        # using of real objects until EnvironmentManager
        # has loaded them all.
        self._packages = []
        self._vms = []
        self.providers = []
        self.vm_providers = []

        self.active_package = None
        self.avaliable_vms = []

        self.min_target = None
        self.loaded = False

        if self._file:
            self._config = EnvFileParser(file).get_config()

            if "PROVIDERS" in self._config:
                self.providers = self._config["PROVIDERS"].split(' ')

            if "VM" in self._config:
                self.vm_providers = self._config["VM"].split(' ')
        else:
            self._config = {}

        # Refactored to make __init__ smaller.
        self.load_providers(self.providers, self.vm_providers)

    def load_providers(self, temp_packages, vms):
        # Now load system pref.  Really should support
        # List of packages instead of single package.
        all_prefs = self._manager.get_virtuals_pref().get_config()
        if self.name() in all_prefs:
            if all_prefs[self.name()] in temp_packages:
                self._packages.append(all_prefs[self.name()])
        else:
            if 'PREFER_UPSTREAM' in all_prefs:
                for package in temp_packages:
                    if re.compile(all_prefs['PREFER_UPSTREAM'] + '*').match(package):
                        self._packages.append(package)
                        break

        for element in temp_packages:
            if not element in self._packages:
                self._packages.append(element)

        verman = VersionManager(self._manager)
        vmachines = self._manager.get_virtual_machines()
        for vm in vmachines:
            if verman.version_satisfies(" ".join(vms), vmachines[vm]):
                self._vms.append(vmachines[vm].name())

        for vm in vms:
            if self._manager.get_vm(vm):
                self._vms.append(vm)
                if not self.min_target:
                    self.min_target = self._manager.get_vm(vm).version()
                if verman.version_cmp(self.min_target, self._manager.get_vm(vm).version()) > 0:
                    self.min_target = self._manager.get_vm(vm).version()

        if not self._packages and not self._vms:
            raise ProviderUnavailableError( self._name, ' '.join(self.vm_providers), ' '.join(self.providers) )

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

    def use_all_available(self):
        if 'MULTI_PROVIDER' in self._config:
            return 'true' == self._config['MULTI_PROVIDER'].lower()
        return False

    def get_vms(self):
        return self._vms

    def get_available_vms(self):
        return self._vms

    def target(self):
        """
        Returns this virtual's target.
        """
        if self.min_target:
            return self.min_target
        try:
            return self.get_provider().query("TARGET")
        except EnvironmentUndefinedError:
            return self.get_provider().query("PROVIDES_VERSION")


    def classpath(self):
        """
        Returns this package's classpath
        """
        if not self.use_all_available():
            try:
                return self.get_provider().classpath()
            except:
                active_vm = self._manager.get_active_vm()
                if active_vm and self.get_available_vms().count(active_vm.name()):
                    if "VM_CLASSPATH" in self._config:
                        return self._manager.get_active_vm().query('JAVA_HOME') + self._config["VM_CLASSPATH"]
                else:
                    raise ProviderUnavailableError( self._name, ' '.join(self.vm_providers), ' '.join(self.providers) )
        else:
            cp = self.query_all_providers('CLASSPATH')
            if self._vms and not self._manager.get_active_vm().name() in self._vms:
                raise ProviderUnavailableError( self._name, ' '.join(self.vm_providers), ' '.join(self.providers) )

            if "VM_CLASSPATH" in self._config:
                cp += ':' + self._manager.get_active_vm().query('JAVA_HOME') + self._config["VM_CLASSPATH"]
            return cp
        return ""

    def library_path(self):
        try:
            if self.use_all_available():
                return self.query_all_providers('LIBRARY_PATH')
            else:
                return self.get_provider().query('LIBRARY_PATH')
        except EnvironmentUndefinedError:
            return ""

    def query_all_providers(self, var):
        paths = []
        for pkg in self._packages:
            try:
                opkg = self._manager.get_package(pkg)
                paths.append(opkg.query(var))
            except:
                continue
        return ":".join(paths).replace('::', ':').strip(':')


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
        if var == "LIBRARY_PATH":
            return self.library_path()

        return self.get_provider().query(var)

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

    def get_provider(self):
        """
        Return whether a package is to be used by the Virtual.
        """
        if not self.loaded:
            self.load()

        if not len(self._vms) and not self.active_package:
            raise ProviderUnavailableError( self._name, ' '.join(self.vm_providers), ' '.join(self.providers) ) 

        # If no vm's then use active_package
        if not len(self._vms) and self.active_package:
            return self.active_package

        if len(self._vms):
            vm = self._manager.get_active_vm()
            try:
                if self._vms.count(vm.name()):
                    return vm
            except ValueError:
                if not self.active_package:
                    available = ""
                    for vm in self._vms:
                        available = vm + "\n"
                        raise ProviderUnavailableError( self._name, ' '.join(self.vm_providers), ' '.join(self.providers) )
        return self.active_package

    def load(self):
        # Active package is the first available package
        # We load on first use of this Virtual to delay
        # using manager.get_package().
        # This was because manager loaded all packages
        # has been updated to only load packages on demand so
        # this might be redundant.
        for package in self._packages:
            try:
                self.active_package = self._manager.get_package(package)
                self.min_target = self.active_package.query("TARGET")
                break
            except:
                continue
        #Set loaded to true, so functions can determine what is going on
        self.loaded = True

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap :
