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
class VersionManager:
    #atom_parser = re.compile(r"([~!<>=]*)virtual/(jre|jdk)-([0-9\.]+)")
    atom_parser = re.compile(r"([!<>=]+)virtual/(jre|jdk)-([0-9\.*]+)")
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

        return matched_atoms

    def matches(self, version_a, version_b, operator):
        #print "matches: %s %s %s" % (version_a, version_b, operator)
        val = self.version_cmp(version_a, version_b)
        #print "val: %f" % (val)
        if operator == '!': 
            rop = '!='
        else:
            rop = operator.replace('!','')
            if rop == '=':
                rop = '=='

        res = eval("%f %s 0" % (val, rop))

        if operator.find('!') is -1:
            return res
        else:
            return not res
        
    def version_satisfies(self, atoms, vm):
        version = vm.version()
        matched_atoms = self.parse_depend(atoms)

        for atom in matched_atoms:
            if vm.is_type(atom['type']):
                if self.matches(version, atom['version'], atom['equality']):
                    return True
        return False

    def get_lowest(self, atoms):
        atoms = self.parse_depend(atoms)
        lowest = None
        for atom in atoms:
            version = atom['version'].strip('*')
            equality = atom['equality']
            if '!' in equality: continue
            if not '=' in equality and '>' in equality: 
                version = version[:-1]+str(int(version[-1])+1)

            if lowest is None: 
                lowest = version
            else:
                if lowest > version:
                    lowest = version

        if lowest:
            return '.'.join(lowest.split('.')[0:2])
        else:
            raise Exception("Couldnt find a jdk dep")

    def get_vm(self, atoms):
        matched_atoms = self.parse_depend(atoms)

        if len(matched_atoms) == 0:
            return None

        prefs = self.get_prefs()

        low = self.get_lowest(atoms)
        
        vm_list_b = []
        for pref in prefs:
            if pref[0] == low or pref[0] == "*":
                for vm in pref[1]:
                    vm_list = EnvironmentManager().find_vm(vm)
                    vm_list.sort()
                    vm_list.reverse()
                    for vm in vm_list:
                        vm_list_b.append(vm)
        #print "prefs: " + str([vm.name() for vm in vm_list_b])
 
        vm = self.find_matching_vm(vm_list_b, matched_atoms)
        if vm:
            return vm
        else:
            vms = EnvironmentManager().get_virtual_machines().values()
            vms.sort()
            vms.reverse()
            vm = self.find_matching_vm(vms, matched_atoms)
            if vm:
                return vm
            else:
                raise Exception("Couldnt find suitable VM, possible Invalid dep string")

    def find_matching_vm(self, vm_list, atoms):
        cur_good = False
        for vm in vm_list:
            #print "testing: " + str(vm)
            for atom in atoms:
                version = atom['version']
                eq = atom['equality']
                type = atom['type']

                #print "\t %s %s" % (eq, version)
                
                if self.matches(vm.version(), atom['version'], atom['equality']):
                    #print "good"
                    cur_good = True
                else:
                    #print "bad"
                    cur_good = False
                    break 

            if cur_good:
                return vm

        return None

    def find_vm(self, vm, atom):
        vm_list = EnvironmentManager().find_vm(vm)
        vm_list.sort()
        vm_list.reverse()
        for vm in vm_list:
            if vm.is_type(atom['type']) and self.matches(vm.version(), atom['version'], atom['equality']):
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
#            "!=virtual/jdk-1.3 =virtual/jdk-1.4",
#            "=virtual/jdk-1.4 =virtual/jdk-1.3",
#            "!=virtual/jdk-1.5 !=virtual/jdk-1.4 >=virtual/jdk-1.3",
#            "!=virtual/jdk-1.4 =virtual/jdk-1.3*",
#            "=virtual/jdk-1.5*",
#            "=virtual/jdk-1.4*",
#            ">=virtual/jdk-1.3.1* !>=virtual/jdk-1.4",
#            ">=virtual/jdk-1.3.1* !=virtual/jdk-1.4*"
#        ]:
#    rint i
#    try:
#    print vator.get_vm(i)
#    except Exception, ex:
#        print ex
#    print

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
