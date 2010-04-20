# -*- coding: UTF-8 -*-

# Copyright 2004-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from .OutputFormatter import *
from .Package import *
from .Virtual import *
from .VM import *
from .Errors import *

from os.path import basename, dirname
from glob import glob
import os, re, sys

class EnvironmentManager(object):
    """This is the central class, which manages all information from the 'environment'"""
    virtual_machines = None
    virtuals = None
    virtuals_pref = None
    active = None

    # Location of the vm ev files
    vms_path = '/usr/share/java-config-2/vm'
    # Location of the package env files to load
    pkg_path = '/usr/share/%s/package.env'
    virtual_path = '/usr/share/java-config-2/virtuals/'

    system_config_path="/etc/java-config-2/"

    def __init__(self):
        self.all_packages_loaded = False
        self.packages = {}
        self.virtuals = {}

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
                except InvalidVMError as ex:
                    printer = OutputFormatter()
                    printer._printAlert("Invalid vm configuration file found: %s\nJava-config 2 requires some new variables, please update all your jdk/jre:  file\n(%s)" % ( conf, ex ))
                    continue

                self.virtual_machines[count] = vm
                count += 1


    def load_package(self, name):
        try:
            name = name.replace(':', '-')
            pkg = Package(name, sorted (glob (self.pkg_path % name ), reverse=True)[0])
            self.packages[name] = pkg
            return pkg
        except (IndexError, InvalidConfigError):
            try:
                #Try load Virtual instead of Package.
                pkg = Virtual( name, self, self.virtual_path + name )
                self.packages[name] = pkg
                self.virtuals[name] = pkg
                return pkg
            except InvalidConfigError:
                raise UnexistingPackageError(name)

    def load_packages(self):
        for package in iter(glob(self.pkg_path % "*" )):
            name = basename(dirname(package))
            if name in self.packages:
                continue
            self.packages[name] = Package(name, package)

        self.all_packages_loaded = True

        for virtual in iter(glob(self.virtual_path + '*')):
            virt = Virtual(basename(virtual), self, virtual)
            self.packages[virt.name()] = virt
            self.virtuals[virt.name()] = virt

    def get_virtuals_pref(self):
        if self.virtuals_pref is None:
            self.load_virtuals_pref()
        return self.virtuals_pref

    def load_virtuals_pref(self):
        self.virtuals_pref = EnvFileParser(self.system_config_path + "virtuals")

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
        raise InvalidVMError("Unable to determine valid vm. Please see http://www.gentoo.org/doc/en/java.xml#doc_chap4")

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
        for id, vm in self.get_virtual_machines().items():
            # match either exact given string or the unversioned part - bug #288695
            if not name or len(name) == 0:
                found.append(vm)
            elif vm.name() == name:
                found.append(vm)
            elif vm.name() == (name + "-" + vm.version()):
                found.append(vm)
        return found

    def get_package(self, pkgname):
        try:
            return self.packages[pkgname]
        except KeyError:
            if not self.all_packages_loaded:
                return self.load_package(pkgname)

    def get_packages(self):
        """
        Returns a dictionary of Packages indexed by their names.
        For java-config-3 we probably want to change this to return
        the list of packages directly.
        """
        if not self.all_packages_loaded:
            self.load_packages()
        return self.packages

    def get_virtuals(self):
        if self.virtuals is None:
            self.load_packages()
        return self.virtuals

    def get_virtual(self, virtname):
        return self.get_package(virtname)

    def query_packages(self, packages, query):
        results = []
            
        for package in packages:
            pkg = self.get_package(package)
            if pkg:
                value = pkg.query(query)
                if value:
                    results.append(value)
            else:
                raise UnexistingPackageError(package)

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
            for (item, value) in vm.get_config().items():
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
        elif os.path.exists(target):
            raise InvalidConfigError(target)

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
        path = set()
        for lpath in self.query_packages(pkgs, query):
            self.add_path_elements(lpath, path)

        return path

    def build_classpath(self, pkgs):
        return self.build_path(pkgs, "CLASSPATH")

    def get_pkg_deps(self, pkg):
        """
        Returns list of package's deps and optional deps.
        Filters out optional deps that are not present.
        """
        deps = pkg.deps();

        #if hasattr(pkg, 'get_packages') and pkg.use_all_available():
        #    vps = pkg.get_packages()
        #    for vp in vps:
        #        try:
        #            vp_pkg = self.get_package(vp)
        #            deps.append([vp])
        #            deps.append( self.get_pkg_deps(vp) )
        #            print deps
        #        except UnexistingPackageError:
        #            continue
        for opt_dep in pkg.opt_deps():
            try:
                self.get_package(opt_dep[-1])
                deps.append(opt_dep)
            except UnexistingPackageError:
                continue
        return deps

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
        path = set()

        unresolved = set()
        resolved = set()

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

            for dep in self.get_pkg_deps(pkg):
                p = self.get_package(dep[-1])

                if p:
                    if p not in resolved:
                        unresolved.add(p)
                    if query == "CLASSPATH":
                        self.add_dep_classpath(p, dep, path)
                else:
                    missing_deps.add(dep[-1])

        return path

    def add_pkg_env_vars(self, pkg, env):
        """
        Adds variables declared in `pkg`'s package.env via ENV_VARS
        into the dictionary `env`
        """
        env_vars = pkg.query("ENV_VARS")
        if (env_vars):
            for var in env_vars.split(' '):
                val = pkg.query(var)
                assert val
                if (var not in env):
                    env[var] = val

    def build_dep_env_vars(self, pkgs, missing_deps):
        """
        Returns a dictionary of variables declared via ENV_VARS in
        package.env of all packages in list `pkgs` and all dependencies.
        Encountered missing dependencies are recorded in `missing_deps`.
        """
        env = {}

        unresolved = set()
        resolved = set()

        for p in pkgs:
            pkg = self.get_package(p)
            if pkg:
                if hasattr(pkg, 'is_vm') and pkg.is_vm():
                    continue
                pkgs.remove(p)
                unresolved.add(pkg)

        while len(unresolved) > 0:
            pkg = unresolved.pop()
            resolved.add(pkg)

            self.add_pkg_env_vars(pkg, env)

            for dep in self.get_pkg_deps(pkg):
                p = self.get_package(dep[-1])

                if p:
                    if p not in resolved:
                        if hasattr(p, 'is_vm') and p.is_vm():
                            continue
                        unresolved.add(p)
                else:
                    missing_deps.add(dep[-1])
        return env

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

    def have_provider(self, virtuals, virtualMachine, versionManager):
        result=True
        storeVM = self.get_active_vm()
        self.set_active_vm(virtualMachine)
        try:
            for virtualKey in virtuals.split():
                if self.get_package(virtualKey):
                    try:
                        self.get_package(virtualKey).get_provider().classpath()
                        result= (result and True)
                        continue
                    except AttributeError:
                        if not self.get_package(virtualKey).get_available_vms().count(virtualMachine.name()) > 0:
                            result = False
                        else:
                            result=result and True
        finally:
            self.set_active_vm(storeVM)
        return result
    
# Singleton hack 
EnvironmentManager = EnvironmentManager()

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
