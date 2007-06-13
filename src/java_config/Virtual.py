# -*- coding: UTF-8 -*-

# Copyright 2004-2007 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from FileParser import *

class Virtual:
    """
    Class represeting an installed java virtual.
    """
    _packages = []
    active_package = None

    def __init__(self, name, manager, file = None):
        self._file = file
        self._name = name
	self._manager = manager
	temp_packages = []
        if self._file:
            self._config = EnvFileParser(file).get_config()
	    temp_packages = self._config["PROVIDERS"].split(' ')
        else:
            self._config = {}
	#Now load system pref
	all_prefs = self._manager.get_virtuals_pref().get_config()
	if all_prefs.has_key(self.name()):
	    if all_pref[self.name()].name() in temp_packages:
		self._packages.append(all_pref[self.name()])
	
	for element in temp_packages:
	    if not element in self._packages:
	    	self._packages.append(element)
	# Dont load active_package now, we may want active_package
	# To be another, yet unloaded, (virtual) package.
		
    def __str__(self):
        return self.name()

    def name(self):
        #return self.get_active_package().name()
	return self._name

    def file(self):
    	# Investigate if anything uses this
	# and whether what it should therefore return.
        return self._file

    def description(self):
        #if self._config.has_key("DESCRIPTION"):
        #    return self._config["DESCRIPTION"]
        #else:
        #    return "No Description"
	return self.get_active_package().description()

    def get_packages(self):
    	return self._packages

    def classpath(self):
        """
        Returns this package's classpath
        """
        #if self._config.has_key("CLASSPATH"):
        #    return self._config["CLASSPATH"]
        #else:
        #    return None
	return self.get_active_package().classpath()

    def query(self, var):
        """
        Return the value of the requested var form the env file
        """
	return self.get_active_package().query(var)
        #if self._config.has_key(var):
        #    return self._config[var]
        #else:
        #    return None


    def deps(self):
        """
        Return all packages this package depends on
        """
        return self.get_active_package().deps()
	#depstr = self.query("DEPEND")
        #if depstr:
        #    return [dep.split("@") for dep in depstr.split(":")]
        #else:
        #    return []

    def provides(self):
        """
        Return the virtuals this package provides
        """
        return self.get_active_package().provides()
	#pv = self.query('PROVIDES')
        #if pv:
        #    return pv.split(" ")
        #return []

    def get_active_package(self):
    	if self.active_package is None:
	    self.load_active_package()
	return self.active_package

    def load_active_package(self):
    	# Active package is the first available package.
	for package in self._packages:
	    if self._manager.get_package(package) is not None :
	    	self.active_package = self._manager.get_package(package)
	
	if self.active_package is None:
	    #Eventually this should throw an error?
	    self.active_package = Package("No package provided")


# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
