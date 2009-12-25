# -*- coding: UTF-8 -*-

# Copyright 2004-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from .FileParser import *

class Package:
    """
    Class represeting an installed java package
    """
    def __init__(self, name, file = None):
        self._file = file
        self._name = name
        if self._file:
            self._config = EnvFileParser(file).get_config()
        else:
            self._config = {}

    def __str__(self):
        return self.name()

    def name(self):
        return self._name

    def file(self):
        return self._file

    def description(self):
        if "DESCRIPTION" in self._config:
            return self._config["DESCRIPTION"]
        else:
            return "No Description"

    def classpath(self):
        """
        Returns this package's classpath
        """
        if "CLASSPATH" in self._config:
            return self._config["CLASSPATH"]
        else:
            return None

    def target(self):
        return self.query("TARGET")
    
    def query(self, var):
        """
        Return the value of the requested var form the env file
        """
        if var in self._config:
            return self._config[var]
        else:
            return None

    def deps(self):
        """
        Return all packages this package depends on
        """
        return self.__get_deps("DEPEND")
        
    def opt_deps(self):
        """
        Return all packages this package optionally depends on
        """
        return self.__get_deps("OPTIONAL_DEPEND")

    def get_provides(self):
        """
        Return the virtuals this package provides
        """
        pv = self.query('PROVIDES')
        if pv:
            return pv.split(" ")
        return []
    
    def __get_deps(self, query):
        """
        Internal function to get package's (optional) dependencies;
        @param query: variable to read from package.env
        """
        depstr = self.query(query)
        if depstr:
            return [dep.split("@") for dep in depstr.split(":")]
        else:
            return []

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
