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

class VM:

   def __init__(self, file, active=False):
      self.file = file
      self.active = active
      self.config = {}

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

   def config(self):
      return self.config

   def query(self,var):
      if self.config.has_key(var):
         return self.config[var]
      else:
         raise JavaErrors.EnvironmentUndefinedError

   def active(self):
      return self.active

   def set_active(self):
      self.active = True

   def filename(self):
      return self.file

   def name(self):
      # TODO: MAKE THIS MODULAR!
      return self.file.lstrip("/etc/env.d/java/20")

   def is_jre(self):
      # TODO: REMOVE THIS HACK FOR BACKWARDS COMPATIBILITY
      if self.config.has_key('PROVIDES_TYPE'):
         return self.type("JRE")
      else:
         if self.config.has_key('JRE_HOME'):
            return True
      return False

   def is_jdk(self):
      # TODO: REMOVE THIS HACK FOR BACKWARDS COMPATIBILITY
      if self.config.has_key('PROVIDES_TYPE'):
         return self.type("JDK")
      else:
         if self.config.has_key('JDK_HOME'):
            return True
      return False

   def type(self, type):
      if self.query('PROVIDES_TYPE') == type:
         return True
      else:
         return False

   def find_exec(self, executable):
      path = None

      # TODO: REMOVE THIS HACK FOR BACKWARDS COMPATIBILITY
      try:
         path = self.query('PATH')
      except JavaErrors.EnvironmentUndefinedError:
         path = self.query('ADDPATH')

      paths = path.split(':')

      for path in paths:
         path = os.path.join(path, executable)

         if os.path.isfile(path):
            if not os.access(path, os.X_OK):
               raise JavaErrors.PermissionError
            else:
               return path
         else:
            raise JavaErrors.PermissionError
      return None

# vim:set expandtab tabstop=3 shiftwidth=3 softtabstop=3:
