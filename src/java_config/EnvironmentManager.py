# -*- coding: UTF-8 -*-

# Copyright 2004-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from OutputFormatter import *
from Package import *
from VM import *
from Errors import *

from os.path import basename, dirname
from glob import glob
from sets import Set
import os, re, sys

class EnvironmentManager:
    """This is the central class, which manages all information from the 'environment'"""
    virtual_machines = None
    packages = None
    virtuals = None
    active = None

    # Location of the vm ev files
    vms_path = '/usr/share/java-config-2/vm'
    # Location of the package env files to load
    pkg_path = '/usr/share/*/package.env'

    def __init__(self):
        pass

    def __call__(self):
        return self

    def load_vms(self):
        """Load all the vm files, and check for correctness"""
        self.virtual_machines = {} 

        if os.path.isdir(self.vms_path):
            count = 1
            filelist = os.listdir(self.vms_path)
            filelist.sort()
            for file in filelist:
                conf = os.path.join(self.vms_path,file)
                vm = None

                try:
                    vm = VM(conf)
                except InvalidConfigError:
                    continue
                except PermissionError:
                    continue
                except InvalidVMError, ex:
                    printer = OutputFormatter()
                    printer._printAlert("Invalid vm configuration file found: %s\nJava-config 2 requires some new variables, please update all your jdk/jre:  file\n(%s)" % ( conf, ex ))
                    continue

                self.virtual_machines[count] = vm
                count += 1

    def load_packages(self):
        self.packages = {}
        self.virtuals = {}
        for package in iter(glob(self.pkg_path)):
            pkg = Package(basename(dirname(package)), package)
            self.packages[pkg.name()] = pkg

            for virt in pkg.provides():
                if self.virtuals.has_key(virt):
                    self.virtuals[virt].append(pkg)
                else:
                    self.virtuals[virt] = [pkg]

        virtual_prefs = {}
        try:
            vprefs = EnvFileParser("/etc/java-config-2/virtuals")
            virtual_prefs = vprefs.get_config()
        except:
            pass

        for virt, providers in self.virtuals.iteritems():
            if virtual_prefs.has_key(virt):
                pref = virtual_prefs[virt]
                for pkg in providers:
                    if pkg.name() == pref:
                        self.packages[virt] = pkg
            else:
                self.packages[virt] = providers[0]

        for virt in self.get_active_vm().get_provides():
            self.packages[virt] = Package("Provided by the active vm")

    def load_active_vm(self):
        vm_name = os.getenv("GENTOO_VM")
        if vm_name:
            vm = self.get_vm(vm_name)
            if vm:
                self.active = vm
                return vm

        for link in self.vm_links():
            if os.path.islink(link):
                vm_name = basename(os.readlink(link))
                vm = self.get_vm(vm_name)
                if vm:
                    self.active = vm
                    return vm

        raise InvalidVMError

    def set_active_vm(self, vm):
        self.active = vm
 
    def get_active_vm(self):
        if self.active is None:
            self.load_active_vm()
        return self.active

    def get_virtual_machines(self):
        if self.virtual_machines is None:
            self.load_vms()
        return self.virtual_machines

    def find_vm(self, name):
        found = []
        for id, vm in self.get_virtual_machines().iteritems():
            if vm.name().startswith(name):
                found.append(vm)
        return found

    def get_package(self, pkgname):
        all_pkg = self.get_packages()
        if all_pkg.has_key(pkgname):
            return all_pkg[pkgname]
        else:
            return  None

    def get_packages(self):
        if self.packages is None:
            self.load_packages()
        return self.packages

    def get_virtuals(self):
        if self.virtuals is None:
            self.load_packages()
        return self.virtuals

    def query_packages(self, packages, query):
        results = []
        all_pkg = self.get_packages()
        for package in packages[:]:
            if all_pkg.has_key(package):
                packages.remove(package)
                value = all_pkg[package].query(query)
                if value:
                    results.append(value)

        return results

    def get_vm(self, machine):
        vm_list = self.get_virtual_machines()
        selected = None

        for count in iter(vm_list):
            vm = vm_list[count]

            if str(machine).isdigit():
                if int(machine) is count:
                    return vm
            else:
                # Check if the vm is specified via env file
                if machine == vm.filename():
                    return vm 

                # Check if the vm is specified by name 
                if machine == vm.name():
                    return vm

                # Check if the vm is specified via JAVA_HOME
                if machine == vm.query('JAVA_HOME'):
                    return vm

                # Check if vm is specified by partial name 
                if vm.name().startswith(machine):
                    selected = vm

        if selected:
            return selected
        else:
            return None

    def create_env_entry(self, vm, stream, render="%s=%s\n"):
        stream.write("# Autogenerated by java-config\n")
        stream.write("# Java Virtual Machine: %s\n\n" % vm.query('VERSION'))

        try:
            ENV_VARS = vm.query('ENV_VARS')
            for (item, value) in vm.get_config().iteritems():
                if item in ENV_VARS:
                    stream.write(render % (item, value))
        except IOError:
            raise PermissionError
        except EnvironmentUndefinedError:
            raise EnvironmentUndefinedError
 
    def set_user_vm(self, vm):
        self.set_vm(vm, self.user_vm_link())

    def set_system_vm(self, vm):
        self.set_vm(vm, self.system_vm_link())

    def set_vm(self, vm, target):
        sym_dir = dirname(target)
        if not os.path.isdir(sym_dir):
            os.makedirs(sym_dir)

        if os.path.islink(target):
            os.remove(target)

        os.symlink('/usr/lib/jvm/'+vm.name(),target)

    def vm_links(self):
        # Don't try to use user-vm if HOME is undefined
        if os.environ.get('HOME') == None:
            return [ self.system_vm_link() ]
        else:
            return [ self.user_vm_link(), self.system_vm_link() ]

    def user_vm_link(self):
        return  os.path.join(os.environ.get('HOME'), '.gentoo/java-config-2/current-user-vm')

    def system_vm_link(self):
        return '/etc/java-config-2/current-system-vm'

    def clean_classpath(self, targets):
        for target in targets:
            if os.path.isfile(target['file']):
                try:
                    os.remove(target['file'])
                except IOError:
                    raise PermissionError

    def add_path_elements(self, elements, path):
        if elements:
            for p in elements.split(':'):
                if p != '':
                    path.add(p)

    def build_path(self, pkgs, query):
        path = Set()
        for lpath in self.query_packages(pkgs, query):
            self.add_path_elements(lpath, path)

        return path

    def build_classpath(self, pkgs):
        return self.build_path(pkgs, "CLASSPATH")

    def add_dep_classpath(self, pkg, dep, classpath): 
        pkg_cp = pkg.classpath()
        if pkg_cp:
            if not dep or len(dep) == 1:
                self.add_path_elements(pkg_cp, classpath)
            else:
                for cp in pkg_cp.split(':'):
                    if basename(cp) == dep[0]:
                        classpath.add(cp)

    def build_dep_path(self, pkgs, query, missing_deps):
        path = Set()

        unresolved = Set()
        resolved = Set()

        for p in pkgs[:]:
            pkg = self.get_package(p)
            if pkg:
                pkgs.remove(p)
                lpath = pkg.query(query)
                self.add_path_elements(lpath, path)
                unresolved.add(pkg)

        while len(unresolved) > 0:
            pkg = unresolved.pop()
            resolved.add(pkg)

            if query != "CLASSPATH":
                lpath = pkg.query(query)
                self.add_path_elements(lpath, path)

            for dep in pkg.deps():
                p = self.get_package(dep[-1])

                if p:
                    if p not in resolved:
                        unresolved.add(p)
                    if query == "CLASSPATH":
                        self.add_dep_classpath(p, dep, path)
                else:
                    missing_deps.add(dep[-1])

        return path

    def set_classpath(self, targets, pkgs):
        classpath = self.build_classpath(pkgs)

        if classpath:
            self.clean_classpath(targets)

            self.write_classpath(targets, classpath)

    def get_old_classpath(self, target):
        """Returns the current set classpath in the file"""
        oldClasspath = ''
        if os.path.isfile(target['file']):
            try:
                stream = open(target['file'], 'r')
            except IOError:
                raise PermissionError

            for line in stream:
                line = line.strip(' \n')
                if line.find('CLASSPATH') != -1:
                    try:
                        oldClasspath = line.split(target['format'].split('%s')[-2])[-1].strip()
                    except:
                        pass
            stream.close()

        return oldClasspath

    def append_classpath(self, targets, pkgs):
        classpath = self.build_classpath(pkgs)

        if classpath:
            oldClasspath = None
            for target in targets:
                for cp in self.get_old_classpath(target).split(':'):
                    classpath.add(cp)

            self.clean_classpath(targets)

            self.write_classpath(targets, classpath)

    def write_classpath(self, targets, classpath):
        for target in targets:
            dir = dirname(target['file'])
            if not os.path.isdir(dir):
                os.makedirs(dir)

            try:
                stream = open(target['file'], 'w')
            except IOError:
                raise PermissionError

            stream.write(target['format'] % ("CLASSPATH", ':'.join(classpath)))
            stream.close()

    def have_provider(self, virtuals):
        for virtual in virtuals.split():
            if not self.get_virtuals().has_key(virtual):
                return False

        return True

# Singleton hack 
EnvironmentManager = EnvironmentManager()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
