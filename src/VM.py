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

import EnvFileParser
import os

from Errors import *

class VM:

   def __init__(self, file, active=False):
      self.file = file
      self.active = active
      self.config = EnvFileParser.EnvFileParser(file).get_config()

   def __cmp__(self, other):
      return cmp(self.version(), other.version())

   def __str__(self):
      return self.name()

   def get_config(self):
      return self.config

   def query(self,var):
      if self.config.has_key(var):
         return self.config[var]
      else:
         print "Undefined: " + var
         raise EnvironmentUndefinedError

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
      return self.is_type("JRE")

   def is_jdk(self):
      return self.is_type("JDK")

   def is_type(self, type):
      if self.query('PROVIDES_TYPE') == type:
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

# vim:set expandtab tabstop=3 shiftwidth=3 softtabstop=3:
