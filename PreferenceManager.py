# -*- coding: UTF-8 -*-

# Copyright 2004 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

# Author: Saleem Abdulrasool <compnerd@gentoo.org>
# Maintainer: Gentoo Java Herd <java@gentoo.org>
# Java Subsystem Configuration Utility for Gentoo Linux

# ChangeLog
# Saleem A. <compnerd@gentoo.org>
#     April 19, 2005 - Initial Write

import VM,Errors,versionator
import os,glob,re

class PreferenceManager:
   def __init__(self):
      self.database = os.path.join('/', 'var', 'db', 'java')
      self.java_versions = [ '1.0', '1.1', '1.2', '1.3', '1.4', '1.5' ]

   def create_database(self):
      if not os.path.exists(self.database):
         try:
            os.makedirs(os.path.dirname(self.database))
         except IOError:
            raise PermissionError

      for java_version in java_versions:
         file = os.path.join(self.database, java_version)
         if not os.path.isfile(file):
            stream = open(file,'w')
            stream.write("# Java Virtual Machine Preferences")
            stream.close()

   def get_preferred_vm(self, version, level='0'):
      file = os.path.join(self.database, version)

      if os.path.isfile(file):
         prefs = PrefsFileParser(file).get_prefs()
         return prefs[level]
      else:
         raise InvalidPrefsFileError

   def set_preferred_vm(self, version, vm):
      file = os.path.join(self.database, version)
      prefs = {} 

      if os.path.isfile(file):
         prefs = PrefsFileParser(file).get_prefs()

      index = 0
      for key,value in prefs.iteritems():
         if value == vm:
            index = key
            break

      while index > 0:
         prefs[index+1] = prefs[index]
         index -= 1
      prefs[0] = vm

      write_prefs(file, prefs)

   def remove_preferred_vm(self, version, vm):
      file = os.path.join(self.database, version)
      prefs = {}

      if os.path.isfile(file):
         prefs = PrefsFileParser(file).get_prefs()
      
      for key,value in prefs.iteritems():
         if value == vm:
            del prefs[key]
            break

      write_prefs(file, prefs)

   def write_prefs(self, file, prefs):
      stream = open(file, 'w')
      stream.write("# Java Virtual Machine Preferences")

      length = len(prefs)
      for i in range(0,length):
         stream.write("%i : %s" % (i,prefs[i]))

      stream.close()
