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

__version__ = '$Revision: 2.0$'[11:-1]

import os

import JavaExceptions

class JavaEnvironParser:
   environ_path = [
                     os.path.join(os.environ.get('HOME'), '.gentoo', 'java'),
                     os.path.join('/etc/env.d', '20java')
                  ]

   def __file_query(self, file, query):
      try:
         stream = open(file, 'r')
      except IOError:
         return None

      read = stream.readline()
      while read:
         if read.strip().startswith(query):
            stream.close()
            value = read.split('=', 1)
            return value[-1].strip()
         else:
            read = stream.readline()
      stream.close()
      return None
      
   def query(self, query):
      for env_file in self.environ_path:
         query_result = self.__file_query(env_file, query)
         if query_result != None:
            return query_result
      return None

class EnvironmentManager:
   def __init__(self):
      self.environment = JavaEnvironParser()
      self.JAVA_HOME = self.environment.query('JAVA_HOME')

      if self.JAVA_HOME is None:
         raise JavaExceptions.EnvironmentUndefinedError

   def query_variable(self, variable):
      value = self.environment.query(variable)
      if value is not None:
         return value
      else:
         raise JavaExceptions.EnvironmentUndefinedError

   def find_exec(self, executable, java_home=None):
      if java_home is None:
         java_home = self.JAVA_HOME

      jre_path = java_home + '/bin/' + str(executable)
      jdk_path = java_home + '/jre/bin/' + str(executable)

      if os.path.isfile(jre_path):
         if not os.access(jre_path, os.X_OK):
            raise JavaExceptions.EnvironmentUnexecutableError
         else:
            return jre_path 
      elif os.path.isfile(jdk_path):
         if not os.access(jdk_path, os.X_OK):
            raise JavaExceptions.EnvironmentUnexecutableError
         else:
            return jdk_path 
      else:
            raise JavaExceptions.EnvironmentUnexecutableError

