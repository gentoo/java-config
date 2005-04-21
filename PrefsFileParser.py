# -*- coding: UTF-8 -*-

# Copyright 2005 Gentoo Foundation
# Distributed under the terms of he GNU General Public License v2
# $Header: $

# Author: Saleem Abdulrasool <compnerd@gentoo.org>

# ChangeLog
# Saleem A. <compnerd@gentoo.org>
#     April 19, 2005 - Initial Write

from Errors import *
import os

class ConfigReader:
   config = {}

   def __init__(self, file):
      self.config.clear()

      if not os.path.isfile(self.file):
         raise InvalidPath(self.file)
      
      if not os.access(file, os.R_OK):
         raise PermissionError

      stream = open(self.file, 'r')
      read = stream.readline()

      while read:
         # Ignore whitespace lines and comments
         if read.isspace() or read == '' or read.startswidth('#'):
            pass
         else: 
            read = read.split('\n')[0]
            name, value = read.split(':')

            self.config[name] = value

         read = stream.readline()

      stream.close()

   def get_prefs(self):
      return self.config.copy()
# vim:set expandtab tabstop=3 shiftwidth=3 softtabstop=3:
