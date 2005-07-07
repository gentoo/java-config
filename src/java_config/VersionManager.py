# -*- coding: UTF-8 -*-

# Copyright 2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public license v2
# $Header: $

import re
from string import upper

import VM, Errors 
from java_config.FileParser import *
from java_config.EnvironmentManager import *
import os, glob, re
import os.path


# Does not handle deps correctly in any way
# Does however do the right thing for the only types of deps we should see
# (i hope)
class VersionManager:
    #atom_parser = re.compile(r"(?P<equality>[~!<>=]*)virtual/(?P<environment>jre|jdk)-(?P<version>[0-9\.]+)")
    atom_parser = re.compile(r"(?P<equality>[!<>=]+)virtual/(?P<environment>jre|jdk)-(?P<version>[0-9\.]+)")
    pref_files = ['/etc/java-config/jdk.conf', '/usr/share/java-config/config/jdk-defaults.conf']
    _prefs = None

    def __init__(self):
        pass

    def get_prefs(self):
        if self._prefs:
            return self._prefs
        else:
            self._prefs = []
            for file in self.pref_files:
                if os.path.exists(file):
                    self._prefs += PrefsFileParser(file).get_config()
            return self._prefs

    def parse_depend(self, atoms):
        matched_atoms = []

        matches = self.atom_parser.findall(atoms)

        if len(matches) >  0:
            for match in matches:
                matched_atoms.append({'equality':match[0], 'item':upper(match[1]), 'version':match[2]})

        return matched_atoms

    def matches(self, version_a, version_b, operator):
        if operator == '!': 
            operator = '!='
        if operator == '=': 
            operator = '=='

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
        matched_atoms = self.parse_depend(atoms)

        if len(matched_atoms) == 0:
            return None

        prefs = self.get_prefs()
        low = None

        for atom in matched_atoms:
            version = atom['version']
            eq = atom['equality']

            if low is None:
                low = atom
            elif low['version'] > version:
                low = atom

            for pref in prefs:
                if pref[0] == version or pref[0] == "*":
                    for vm in pref[1]:
                        gvm = self.find_vm(vm, atom)
                        if gvm is not None:
                            return gvm

        return self.find_vm("", low)

    def find_vm(self, vm, atom):
        vm_list = EnvironmentManager().find_vm(vm)
        vm_list.sort()
        vm_list.reverse()
        for vm in vm_list:
            if self.matches(vm.version(), atom['version'], atom['equality']):
                 return vm
        return None
            

vator=VersionManager()
for i in [">=virtual/jdk-1.3",">=virtual/jdk-1.4",">=virtual/jdk-1.5","=virtual/jdk-1.3 =virtual/jdk-1.4","=virtual/jdk-1.5*","=virtual/jdk-1.4*"]:
    print i
    print vator.get_vm(i)
    print


# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
