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
import JavaErrors

class JavaEnvironParser:
   environ_path = [
                     os.path.join(os.environ.get('HOME'), '.gentoo', 'java'),
                     os.path.join('/etc/env.d', '20java')
                  ]

   def query(self, query):
      for file in self.environ_path:
         try:
            stream = open(file, 'r')
         except IOError:
            continue

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

   def config_dict(self, file):
      config = {}
      bracketed = False

      if not os.path.isfile(file) or not os.access(file, os.R_OK):
         return None

      stream = open(file, 'r')
      read = stream.readline()
      while read:
         if read.isspace() or read == '' or read.startswith('#'):
            read = stream.readline()
         else:
            read = read.split('\n')[0]
            read.replace
            name, value = read.split('=')

            if value == '':
               raise JavaErrors.InvalidConfigError(file)

            values = value.split(':')
            for item in values:
               item = item.strip('\\').strip('\'\"')

               if item.find('${') >= 0:
                  bracketed = True
                  item = item[item.find('${')+2:item.find('}')]

               if config.has_key(item):
                  val = config[item]
               else:
                  val = ''
               
               if bracketed:
                  value = value.replace('${%s}' % item, val)
                  bracketed = False
               else:
                  value = value.replace('$%s' % item, val)
            
            config[name] = value

            read = stream.readline()

      stream.close()

      return config

class EnvironmentManager:
   envparser = JavaEnvironParser()
   virtual_machines = {}
   
   def __init__(self):
      # Get the JAVA_HOME
      self.JAVA_HOME = self.envparser.query('JAVA_HOME')
      if self.JAVA_HOME is None:
         raise JavaErrors.EnvironmentUndefinedError

      # Collect the Virtual Machines
      if os.path.isdir('/etc/env.d/java'):
         try:
            count = 1;
            for file in os.listdir('/etc/env.d/java'):
               conf = os.path.join('/etc/env.d/java', file)
               config = self.envparser.config_dict(conf)

               try:
                  if os.path.isdir(config['JAVA_HOME']):
                     self.virtual_machines[(file, count)] = config
               except KeyError:
                  raise JavaErrors.InvalidConfigError(conf)
               count += 1
         except OSError:
            pass

   def find_exec(self, executable, java_home=None):
      if java_home is None:
         java_home = self.JAVA_HOME

      jre_path = java_home + '/bin/' + str(executable)
      jdk_path = java_home + '/jre/bin' + str(executable)

      if os.path.isfile(jre_path):
         if not os.access(jre_path, os.X_OK):
            raise JavaErrors.PermissionError
         else:
            return jre_path
      elif os.path.isfile(jdk_path):
         if not os.access(jdk_path, os.X_OK):
            raise JavaErrors.PermissionError
         else:
            return jdk_path
      else:
         raise JavaErrors.PermissionError

   def query_variable(self, variable):
      value = self.envparser.query(variable)
      if value is None:
         raise JavaErrors.EnvironmentUndefinedError
      else:
         return value

   def get_active_vm(self):
      for vm in self.virtual_machines.keys():
         if (self.virtual_machines[vm]['JAVA_HOME'] == self.JAVA_HOME):
            return vm[2:]

   def is_active_vm(self, java_home):
      if java_home == self.JAVA_HOME:
         return True
      else:
         return False

   def get_virtual_machines(self):
      return self.virtual_machines

   def get_vm_from_home(self, home):
      vm_list = self.get_virtual_machines()

      for vm in iter(vm_list):
         if vm['JAVA_HOME'] == home:
            return vm
      return None

   def get_vm(self, machine):
      vm_list = self.get_virtual_machines()
      selected = None

      for (vm,count) in iter(vm_list):
         if machine[0].isdigit():
            if int(machine[0]) is count:
               return vm_list[(vm,count)]
         else:
            if machine[0] == vm:
               return vm_list[(vm_count)]
            elif machine[0] == vm.lstrip("20"):
               return vm_list[(vm,count)]
            elif vm.lstrip("20").startswith(vm):
               selected = (vm,count)

      if selected:
         return vm_list[selected]
      else:
         return None

   def set_vm(self, java_vm, env_file, javaws_file):
      vm = self.get_vm(java_vm)
 
      try:
         stream = open(env_file, 'w')
      except IOError:
         raise JavaErrors.PermissionError

      stream.write("# Autogenerated by java-config\n")
      stream.write("# Java Virtual Machine: %s\n\n" % vm['VERSION'][1:-1])

      for (item,value) in vm.iteritems():
         try:
            if item in vm["ENV_VARS"]:
               stream.write('%s=%s\n' % (item,value))
            else:
               stream.write('# %s=%s\n' % (item,value))
         except IOError:
            continue

      stream.close()

      # Create the javaws property file
      # Resolves bug #60606

      try:
         if not os.path.exists(javaws_file):
            os.makedirs(os.path.dirname(javaws_file))
         stream = open(javaws_file, 'w')
      except IOError:
         raise JavaErrors.PermissionError

      stream.write("# Autogenerated by java-config\n")
      stream.write("deployment.javaws.jre.0.platform=" + vm['PLATFORM'])
      stream.write("deployment.javaws.jre.0.version=" + vm['VERSION'][-8:0])
      stream.write("deployment.javaws.jre.0.path=" + self.find_exec('java', vm['JAVA_HOME']))

      stream.close()


   def valid_vm(self, machine):
      executables = [ 'javac', 'javadoc', 'jar' ]
      optionals = [ 'rmic' ]
      machine = self.get_vm(machine)

      for exe in executables:
         try:
            self.find_exec(exe, machine['JAVA_HOME']) 
         except:
            raise JavaErrors.InvalidVM

      for exe in optionals:
         try:
            self.find_exec(exe, machine['JAVA_HOME'])
         except:
            raise JavaErrors.MissingOptionals
      
      return True
