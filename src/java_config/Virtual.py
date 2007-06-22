# -*- coding: UTF-8 -*-

# Copyright 2004-2007 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from FileParser import *

class Virtual:
    """
    Class represeting an installed java virtual.
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
        # Now load system pref. Really should support
        # List of packages instead of singular.
        all_prefs = self._manager.get_virtuals_pref().get_config()
        if all_prefs.has_key(self.name()):
            if all_prefs[self.name()] in temp_packages:
                self._packages.append(all_prefs[self.name()])
        for element in temp_packages:
            if not element in self._packages:
                self._packages.append(element)
        # Dont load active_package now, we may want active_package
        # To be another, yet unloaded, (virtual) package.
		
    def __str__(self):
        return self.name()

    def name(self):
        return self._name

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
        return self.get_active_package().classpath()

    def query(self, var):
        """
        Return the value of the requested var form the env file
        """
        return self.get_active_package().query(var)


    def deps(self):
        """
        Return all packages this package depends on
        """
        return self.get_active_package().deps()

    def provides(self):
        """
        Return the virtuals this package provides
        """
        return self.get_active_package().provides()

    def get_active_package(self):
        if self.active_package:
            self.load_active_package()
        return self.active_package

    def load_active_package(self):
        # Active package is the first available package.
        for package in self._packages:
            if self._manager.get_package(package) is not None:
                self.active_package = self._manager.get_package(package)
        if self.active_package:
            #Eventually this should throw an error?
            self.active_package = Package("No package provided.")

#vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
