#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2004-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from .FileParser import *
from .Errors import *
import os


class VM:
    # Dont accept env files without these variables
    needed_vars = [ "JAVA_HOME", "PROVIDES_TYPE", "PROVIDES_VERSION" ]

    def __init__(self, file):
        self.file = file
        self.config = EnvFileParser(file).get_config()
    
        for var in self.needed_vars:
            if var not in self.config:
                raise InvalidVMError("Missing: %s" %var)

    def __eq__(self, other):
        return self.version() == other.version()

    def __ne__(self, other):
        return self.version() != other.version()

    def __lt__(self, other):
        return self.version() < other.version()

    def __gt__(self, other):
        return self.version() > other.version()

    def __le__(self, other):
        return self.version() <= other.version()

    def __ge__(self, other):
        return self.version() >= other.version()

    def __str__(self):
        return self.name()

    def get_config(self):
        return self.config

    def query(self, var):
        if var in self.config:
            return self.config[var]
        else:
            raise EnvironmentUndefinedError

    def filename(self):
        return self.file

    def name(self):
        return os.path.basename(self.file)

    def is_build_only(self):
        try:
            if self.query('BUILD_ONLY').upper() == 'TRUE':
                return True
        except:
            return False

    def is_jre(self):
        return self.is_type("JRE")

    def is_jdk(self):
        return self.is_type("JDK")

    def is_type(self, type):
        if type.upper() in [t.upper() for t in self.query('PROVIDES_TYPE').split(' ')]:
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

    def get_provides(self):
        if 'PROVIDES' in self.config:
            return self.config['PROVIDES'].split(' ')
        return []

    def provides(self, virtuals):
        if 'PROVIDES' in self.config:
            vp = self.config['PROVIDES'].split(' ')
        else:
            return False

        found = 0
        
        for virtual in virtuals:
            if virtual in vp:
                found += 1
            else:
                return False

        return found == len(virtuals)

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
