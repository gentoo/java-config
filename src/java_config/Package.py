# -*- coding: UTF-8 -*-

# Copyright 2004-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from FileParser import *

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
        if self._config.has_key("DESCRIPTION"):
            return self._config["DESCRIPTION"]
        else:
            return "No Description"

    def classpath(self):
        """
        Returns this package's classpath
        """
        if self._config.has_key("CLASSPATH"):
            return self._config["CLASSPATH"]
        else:
            return None

    def query(self, var):
        """
        Return the value of the requested var form the env file
        """
        if self._config.has_key(var):
            return self._config[var]
        else:
            return None

    def deps(self):
        """
        Return all packages this package depeds on
        """
        depstr = self.query("DEPEND")
        if depstr:
            return [dep.split("@") for dep in depstr.split(":")]
        else:
            return []

    def provides(self):
        """
        Return the virtuals this package provides
        """
        pv = self.query('PROVIDES')
        if pv:
            return pv.split(" ")
        return []

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
