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


# Does not handle deps correctly
# Does however do the right thing for the only types of deps we should see
# Ignore blockers: portage doesn't support them in a way that is usefull for us
class VersionManager:
    #atom_parser = re.compile(r"([~!<>=]*)virtual/(jre|jdk)-([0-9\.]+)")
    atom_parser = re.compile(r"([<>=]+)virtual/(jre|jdk)-([0-9\.*]+)")
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
                matched_atoms.append({'equality':match[0], 'type':match[1], 'version':match[2]})

        matched_atoms.sort()
        matched_atoms.reverse()

        return matched_atoms

    def matches(self, version_a, version_b, operator):
        val = self.version_cmp(version_a, version_b)

        if operator == '=':    return val == 0
        elif operator == '>=': return val >= 0
        elif operator == '<=': return val <= 0
        elif operator == '>':  return val > 0
        elif operator == '<':  return val < 0
        else:                  return False
        
    def version_satisfies(self, atoms, vm):
        version = vm.version()
        matched_atoms = self.parse_depend(atoms)

        for atom in matched_atoms:
            if vm.is_type(atom['type']):
                if self.matches(version, atom['version'], atom['equality']):
                    return True
        return False

    def get_lowest_atom(self, atoms):
        lowest = None
        for atom in atoms:
            if not lowest:
                lowest = atom
            else:
                if self.version_cmp(lowest['version'], atom['version']) > 0:
                    lowest = atom

        if lowest:
            return atom
        else:
            raise Exception("Couldnt find a vm dep")

    def get_lowest(self, atoms):
        atoms = self.parse_depend(atoms)
        lowest = self.get_lowest_atom(atoms)
        lowest = lowest['version']

        if lowest:
            return '.'.join(lowest.strip('*').split('.')[0:2])
        else:
            raise Exception("Couldnt find a vm dep")


    def get_vm(self, atoms):
        matched_atoms = self.parse_depend(atoms)

        if len(matched_atoms) == 0:
            return None

        prefs = self.get_prefs()

        low = self.get_lowest(atoms)
        for atom in matched_atoms: 
            for pref in prefs:
                if pref[0] == low or pref[0] == "*":
                    for vm in pref[1]:
                        gvm = self.find_vm(vm, atom)
                        if gvm:
                            return gvm

        low = self.get_lowest_atom(matched_atoms)
        vm = self.find_vm("", low)
        if vm:
            return vm
        else:
            raise Exception("Couldnt find suitable VM, possible Invalid dep string")

    def find_vm(self, vm, atom):
        vm_list = EnvironmentManager().find_vm(vm)
        vm_list.sort()
        vm_list.reverse()
        for vm in vm_list:
            if vm.is_type(atom['type']):
                if self.matches(vm.version(), atom['version'], atom['equality']):
                    return vm
        return None

    def version_cmp(self, version1, version2):
        if version1 == version2:
            return 0

        version1 = version1.split('.')
        version2 = version2.split('.')

        check_len = None
        for x in range(1, len(version1)):
            if version1[x][-1] == '*':
                version1[x] = version1[x][:-1]
                check_len = x
            if version1[x][0] == '0':
                version1[x]='.' + version1[x]

        for x in range(1, len(version2)):
            if version2[x][-1] == '*':
                version2[x] = version2[x][:-1]
                if (not check_len) or (check_len and check_len > x):
                    check_len = x
            if version2[x][0] == '0':
                version2[x]='.' + version2[x]

       
        if len(version2) < len(version1):
            version2.extend(["0"]*(len(version1)-len(version2)))
        elif len(version1) < len(version2):
            version1.extend(["0"]*(len(version2)-len(version1)))

        for x in range(0, len(version1)):
            if check_len and x > check_len:
                return 0
            ret = float(version1[x]) - float(version2[x])
            if ret != 0:
                return ret
        return 0

#vator=VersionManager()
#for i in [  
#            ">=virtual/jdk-1.3",
#            ">=virtual/jdk-1.4",
#            ">=virtual/jdk-1.5",
#            "|| ( =virtual/jdk-1.4* =virtual/jdk-1.3* )",
#            "|| ( =virtual/jdk-1.3* =virtual/jdk-1.4* )",
#            "=virtual/jdk-1.5*",
#            "=virtual/jdk-1.4*",
#            "=virtual/jdk-1.3*",
#        ]:
#    print i
#    try:
#    print vator.get_vm(i)
#    except Exception, ex:
#        print ex
#    print

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
