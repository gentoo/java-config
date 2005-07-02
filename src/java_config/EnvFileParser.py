# -*- coding: UTF-8 -*-

# Copyright 2004-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from Errors import *
import os

class EnvFileParser:
    config = {}
    
    def __init__(self, file):
        self.config.clear()

        # Create the config from the file
        if not os.path.isfile(file):
            raise InvalidConfigError(file)
        if not os.access(file, os.R_OK):
            raise PermissionError

        stream = open(file, 'r')
        for line in stream:
            line = line.strip('\n')
            if line.isspace() or line == '' or line.startswith('#'):
                continue
            else:
                index = line.find('=')
                name = line[:index]
                value = line [index+1:]

                if value == '':
                    raise InvalidConfigError(file)

                value = value.strip('\\\'\"')

                while value.find('${') >= 0:
                    item = value[value.find('${')+2:value.find('}')]

                    if self.config.has_key(item):
                        val = self.config[item]
                    else:
                        val = ''
                        
                    value = value.replace('${%s}' % item, val)
                
                self.config[name] = value

        stream.close()

    def get_config(self):
        return self.config.copy()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
