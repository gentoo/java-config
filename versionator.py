# -*- coding: UTF-8 -*-

# Copyright 2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public license v2
# $Header: $

# Author: Saleem Abdulrasool <compnerd@gentoo.org>
# Maintainer: Gentoo Java Herd <java@gentoo.org>
# Python based utilities

# ChangeLog
# Saleem A. <compnerd@gentoo.org>
#     March 31, 2005 - Initial Write

import re

class versionator:
   def __init__(self):
      self.atom_parser = re.compile(r"(?P<equality>[~!<>=]*)virtual/(?P<environment>jre|jdk)-(?P<version>[0-9\.]+)")
   
   def parse_depend(self, atoms):
      matched_atoms = []

      for atom in atoms.split(','):
         # Remove whitespace
         atom = atom.strip()

         # Parse the atom
         matches = self.atom_parser.findall(atom)

         # Collect only the java atoms
         if len(matches) is not 0:
            for i in range(len(matches)):
               match = matches[i]
               matched_atoms.append({'equality':match[0], 'item':match[1], 'version':match[2]})

      return matched_atoms

   def version_satisfies(self, atoms, item, version):
      matched_atoms = parse_depend(atoms)

      for atom in matched_atoms:
         if atom['item'] == item:
            if matches(atom['version'], version, atom['equality']):
               return true
      return false

   def matches(self, version_a, version_b, operator):
      version_a = version_a.replace('.')
      version_b = version_b.replace('.')

      # Fix the not operator to work with our checker
      if operator = '!':
         operator = '!='

      if operator.find('!') is -1:
         return eval(version_a + operator + version_b)
      else:
         return !(eval(version_a + operator.replace('!', '') + version_b)) 

      return False
