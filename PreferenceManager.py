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
      self.prefs = {}

      load_database()

   def load_database(self):
      if not os.path.exists(self.database):
         create_database()

      for java_version in java_versions:
         file = os.path.join(self.database, java_version)
         self.prefs[version] = PrefsFileParser(file).get_prefs()

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
      if not self.prefs.has_key(version):
         raise InvalidPrefsFileError
         
      if len(self.prefs[version]) is 0:
         raise PrefsUndefinedError
      
      return self.prefs[version][level]

   def set_preferred_vm(self, version, vm):
      file = os.path.join(self.database, version)

      if not self.prefs.has_key(version):
         raise InvalidPrefsFileError

      if len(self.prefs[version]) is 0:
         raise PrefsUndefinedError

      prefs = self.prefs[version]

      index = get_index(prefs, vm)

      if index not -1:
         while index > 0:
            prefs[index + 1] = prefs[index]
            index -= 1
         prefs[0] = vm

      write_prefs(file, prefs)

   def remove_preferred_vm(self, version, vm):
      file = os.path.join(self.database, version)

      if not self.prefs.has_key(version):
         raise InvalidPrefsFileError

      if len(self.prefs[version]) is 0:
         raise PrefsUndefinedError

      prefs = self.prefs[version]
      
      index = get_index(prefs, vm)

      if index not -1:
         while index < len(prefs) - 1:
            prefs[index] = prefs[index + 1]
         del prefs[len(prefs) - 1]

      write_prefs(file, prefs)

   def get_index(self, prefs, key_value):
      for key,value in prefs.iteritems():
         if value == key_value:
            return key
      return -1

   def write_prefs(self, file, prefs):
      stream = open(file, 'w')
      stream.write("# Java Virtual Machine Preferences")

      length = len(prefs)
      for i in range(0,length):
         stream.write("%i : %s" % (i,prefs[i]))

      stream.close()
