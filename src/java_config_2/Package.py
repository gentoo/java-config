# -*- coding: UTF-8 -*-
# Copyright 2004-2013 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

from .FileParser import *

class Package:
    """
    The Package class represents an installed Java package.
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
        """
        Returns this package's name.
        """
        return self._name

    def file(self):
        """
        Returns this package's file.
        """
        return self._file

    def description(self):
        """
        Returns this package's DESCRIPTION.
        """
        if "DESCRIPTION" in self._config:
            return self._config["DESCRIPTION"]
        return "No Description"

    def classpath(self):
        """
        Returns this package's CLASSPATH.
        """
        if "CLASSPATH" in self._config:
            return self._config["CLASSPATH"]
        return None

    def target(self):
        """
        Returns this package's TARGET.
        """
        return self.query("TARGET")

    def query(self, var):
        """
        Return the value of var from the env file.
        """
        if var in self._config:
            return self._config[var]
        else:
            return None

    def deps(self):
        """
        Return all packages this package depends on.
        """
        return self.__get_deps("DEPEND")

    def opt_deps(self):
        """
        Return all packages this package optionally depends on.
        """
        return self.__get_deps("OPTIONAL_DEPEND")

    def __get_deps(self, query):
        """
        Return package's (optional) dependencies;
        @param query: variable to read from package.env
        """
        depstr = self.query(query)
        if depstr:
            return [dep.split("@") for dep in depstr.split(":")]
        else:
            return []

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap: