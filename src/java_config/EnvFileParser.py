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
        read = stream.readline()
        while read:
            if read.isspace() or read == '' or read.startswith('#'):
                read = stream.readline()
            else:
                read = read.split('\n')[0]
                name, value = read.split('=')

                if value == '':
                    raise InvalidConfigError(file)

                value = value.strip('\\').strip('\'\"')

                values  = value.split(':')
                for item in values:
                    if item.find('${') >= 0:
                        item = item[item.find('${')+2:item.find('}')]
                        
                        if self.config.has_key(item):
                            val = self.config[item]
                        else:
                            val = ''
                        
                        value = value.replace('${%s}' % item, val)
                    else:
                        if self.config.has_key(item):
                            val = self.config[item]
                        else:
                            val = ''

                        value = value.replace('$%s' % item, val)

                self.config[name] = value

                read = stream.readline()
        stream.close()

    def get_config(self):
        return self.config.copy()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
