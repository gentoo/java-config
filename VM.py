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

import JavaErrors, EnvFileParser
import os

class VM:

   def __init__(self, file, active=False):
      self.file = file
      self.active = active
      self.config = EnvFileParser.EnvFileParser(file).get_config()

   def get_config(self):
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
