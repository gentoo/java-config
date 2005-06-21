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

import VM,Errors 
from java_config.versionator import *
from java_config.PrefsFileParser import *
from java_config.EnvironmentManager import *
import os,glob,re
import os.path

class PreferenceManager:
	def __init__(self):
		self.pref_files = ['/etc/java-config/jdk.conf', '/usr/share/java-config/config/jdk-defaults.conf']
		self.load()

	def load(self):
		self.prefs = []
		for file in self.pref_files:
			if os.path.exists(file):
				self.prefs = self.prefs + PrefsFile(file).get_prefs()
	

	def get_vm(self, version):
		for pref in self.prefs:
			if pref[0] == version:
				for vm in pref[1]:
					gvm = self.find_vm(vm,version)
					if gvm is not None:
						return gvm
		return self.find_vm("", version)

	def find_vm(self, vm, version):
		vm_list = EnvironmentManager().find_vm(vm)
		#print vm_list
		vm_list.sort()
		vm_list.reverse()
		for vm in vm_list:
			if vm.version() >= version:
			 	return vm
		return None

	
#man=PreferenceManager()
#print "1.3: " + str(man.get_vm("1.3"))
#print "1.4: " + str(man.get_vm("1.4"))
#print "1.5: " + str(man.get_vm("1.5"))
