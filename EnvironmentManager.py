#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2004 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

# Author: Saleem Abdulrasool <compnerd@compnerd.org>
# Maintainer: Gentoo Java Herd <java@gentoo.org>
# Java Subsystem Configuration Utility for Gentoo Linux

# ChangeLog
# Saleem A. <compnerd@compnerd.org>
#     December 30, 2004 - Initial Rewrite
#                       - Based on the collective works of the following:
#                         {karltk,axxo,aether}@gentoo.org

__version__ = '$Revision: 2.0$'[11:-1]

import os

class JavaEnvironParser:
   environ_path = [
                     os.path.join(os.environ.get('HOME'), '.gentoo', 'java'),
                     os.path.join('/etc/env.d', '20java')
                  ]

   def __FileQuery(self, file, query):
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
         query_result = self.__FileQuery(env_file, query)
         if query_result != None:
            return query_result

class EnvironmentManager:
   def __init__(self):
      self.environment = JavaEnvironParser()
      self.java_home = self.environment.query('JAVA_HOME')
