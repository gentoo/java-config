# -*- coding: UTF-8 -*-

# Copyright 2004-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from FileParser import *

class Package:
    def __init__(self, file, name):
        self._file = file
        self._name = name
        self._config = EnvFileParser(file).get_config()

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
        if self._config.has_key("CLASSPATH"):
            return self._config["CLASSPATH"]
        else:
            return None

    def query(self, var):
        if self._config.has_key(var):
            return self._config[var]
        else:
            return None

    def deps(self):
        depstr = self.query("DEPEND")
        if depstr:
            return [dep.split("@") for dep in depstr.split(":")]
        else:
            return []

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
