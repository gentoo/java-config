# -*- coding: UTF-8 -*-
# Copyright 2004-2013 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

from .FileParser import *
from .Errors import *
import os


# Dont accept env files without these variables
NEEDED_VARS = [ "JAVA_HOME", "PROVIDES_TYPE", "PROVIDES_VERSION" ]


class VM:
    def __init__(self, file):
        self.file = file
        self.config = EnvFileParser(file).get_config()
        self.check_for_needed_vars()

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

    def check_for_needed_vars(self):
        for var in NEEDED_VARS:
            if var not in self.config:
                raise InvalidVMError("Missing: %s" % var)

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