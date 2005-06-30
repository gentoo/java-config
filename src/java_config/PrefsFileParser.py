# -*- coding: UTF-8 -*-

# Copyright 2005 Gentoo Foundation
# Distributed under the terms of he GNU General Public License v2
# $Header: $

from Errors import *
import os

class PrefsFile:
    def __init__(self, file):
        self.file = file
        self.config = []

        if not os.path.isfile(self.file):
            raise InvalidConfigError(self.file)

        if not os.access(self.file, os.R_OK):
            raise PermissionError

        stream = open(self.file, 'r')
    
        for line in stream:
            # Ignore whitespace lines and comments
            if line.isspace() or line == '' or line.startswith('#'):
                pass
            else: 
                version, vms = line.split('=')
                vms = vms.strip().split(' ')

                self.config.append([ version, vms ])

        stream.close()

    def get_prefs(self):
        return self.config

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
