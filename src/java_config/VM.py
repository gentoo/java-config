#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2004-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from FileParser import *
from Errors import *
import os
from string import upper


class VM:
    needed_vars = [ "JAVA_HOME", "PROVIDES_TYPE", "PROVIDES_VERSION" ]

    def __init__(self, file):
        self.file = file
        self.config = EnvFileParser(file).get_config()
    
        for var in self.needed_vars:
            if not self.config.has_key(var):
                raise InvalidVMError("Missing: %s" %var)

    def __cmp__(self, other):
        return cmp(self.version(), other.version())

    def __str__(self):
        return self.name()

    def get_config(self):
        return self.config

    def query(self, var):
        if self.config.has_key(var):
            return self.config[var]
        else:
            print "Undefined: " + var
            raise EnvironmentUndefinedError

    def filename(self):
        return self.file

    def name(self):
        # TODO: MAKE THIS MODULAR!
        return self.file.split("/etc/env.d/java/20")[-1]

    def is_jre(self):
        return self.is_type("JRE")

    def is_jdk(self):
        return self.is_type("JDK")

    def is_type(self, type):
        if upper(type) in [upper(t) for t in self.query('PROVIDES_TYPE').split(' ')]:
            return True
        else:
            return False

    def type(self):
        return self.query('PROVIDES_TYPE')

    def version(self):
        return self.query('PROVIDES_VERSION')

    def find_exec(self, executable):
        path = None

        path = self.query('PATH')
        paths = path.split(':')

        for path in paths:
            path = os.path.join(path, executable)

            if os.path.isfile(path):
                if not os.access(path, os.X_OK):
                    raise PermissionError
                else:
                    return path
            else:
                raise PermissionError
        return None

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
