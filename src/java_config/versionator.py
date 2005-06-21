# -*- coding: UTF-8 -*-

# Copyright 2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public license v2
# $Header: $

import re
from string import upper
from java_config.PreferenceManager import *

# Does not handle deps correctly in any way
# Does however do the right thing for the only types of deps we should see
# (i hope)
class versionator:
   def __init__(self):
      #self.atom_parser = re.compile(r"(?P<equality>[~!<>=]*)virtual/(?P<environment>jre|jdk)-(?P<version>[0-9\.]+)")
      self.atom_parser = re.compile(r"(?P<equality>[!<>=]+)virtual/(?P<environment>jre|jdk)-(?P<version>[0-9\.]+)")
   
   def parse_depend(self, atoms):
      matched_atoms = []

      matches = self.atom_parser.findall(atoms)

      if len(matches) >  0:
         for match in matches:
            matched_atoms.append({'equality':match[0], 'item':upper(match[1]), 'version':match[2]})

      return matched_atoms

   def matches(self, version_a, version_b, operator):
      if operator == '!': operator = '!='
      if operator == '=': operator = '=='

      if operator.find('!') is -1:
         return eval(version_a + operator + version_b)
      else:
         return not (eval(version_a + operator.replace('!', '') + version_b)) 

      return False

   def version_satisfies(self, atoms, vm):
      item = upper(vm.type())
      version = vm.version()
      matched_atoms = self.parse_depend(atoms)

      for atom in matched_atoms:
         #print "%s %s %s %s %s" % (item, version, atom['equality'], atom['item'], atom['version'])
         if atom['item'] == item:
            if self.matches(version, atom['version'], atom['equality']):
               return True
      return False

   def get_lowest(self, atoms):
      atoms = self.parse_depend(atoms)
      lowest = None
      for atom in atoms:
         version = atom['version']
         equality = atom['equality']
         if '!' in equality: continue
         if not '=' in equality and '>' in equality: 
            version = version[:-1]+str(int(version[-1])+1)

         if lowest is None: 
            lowest = version
         else:
            if lowest > version:
               lowest = version
      return lowest

   def get_vm(self, atoms):
      lowest = self.get_lowest(atoms)
      return PreferenceManager().get_vm(lowest)

# vim:set expandtab tabstop=3 shiftwidth=3 softtabstop=3:
