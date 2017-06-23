# -*- coding: UTF-8 -*-
# Copyright 2004-2013 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2


from java_config_2.Errors import InvalidConfigError, PermissionError
import os


class FileParser:
    """
    Parse some basic key=value configuration files.
    Values are passed to the pair function.
    """
    def parse(self, file):
        if not os.path.isfile(file):
            raise InvalidConfigError(file)
        if not os.access(file, os.R_OK):
            raise PermissionError

        with open(file, 'r') as stream:
            for line in stream:
                line = line.strip('\n')
                if line.isspace() or line == '' or line.startswith('#'):
                    continue

                index = line.find('=')
                name = line[:index]
                value = line[index+1:]

                if value == '':
                    continue

                value = value.strip('\\\'\"')

                while value.find('${') >= 0:
                    item = value[value.find('${')+2:value.find('}')]

                    if item in self.config:
                        val = self.config[item]
                    else:
                        val = ''
                    value = value.replace('${%s}' % item, val)
                self.pair(name,value)

    def pair(self, key, value):
        pass

class EnvFileParser(FileParser):
    """
    Stores the configuation in a dictionary
    """
    def __init__(self, file):
        self.config = {}
        self.parse(file)

    def pair(self, key, value):
        self.config[key] = value

    def get_config(self):
        return self.config.copy()

class PrefsFileParser(FileParser):
    """
    Stores it in a list.
    """
    def __init__(self, file):
        self.config = []
        self.parse(file)

    def pair(self, key, value):
        self.config.append([key,value.strip('\t ').split(' ')])

    def get_config(self):
        return self.config

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
