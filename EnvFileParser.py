#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2004 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

# Author: Saleem Abdulrasool <compnerd@gentoo.org>
# Maintainer: Gentoo Java Herd <java@gentoo.org>
# Java Subsystem Configuration Utility for Gentoo Linux

# ChangeLog
# Saleem A. <compnerd@gentoo.org>
#     December 30, 2004 - Initial Rewrite
#                       - Based on the collective works of the following:
#                         {karltk,axxo,aether}@gentoo.org

import JavaErrors
import os

class EnvFileParser:
   config = {}
   
   def __init__(self, file):
      # Create the config from the file
      if not os.path.isfile(file):
         raise JavaErrors.InvalidConfigError(file)
      if not os.access(file, os.R_OK):
         raise JavaErrors.PermissionError

      stream = open(file, 'r')
      read = stream.readline()
      while read:
         if read.isspace() or read == '' or read.startswith('#'):
            read = stream.readline()
         else:
            read = read.split('\n')[0]
            name, value = read.split('=')

            if value == '':
               raise JavaErrors.InvalidConfigError(file)

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
      return self.config
