#!/usr/bin/env python

#######################################
package_version = '2.2.0'
#######################################


from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.install import install
from distutils.command.sdist import sdist


import fileinput
import os
import subprocess
import sys
import tempfile
import unittest


class jc_build(build):
	def run(self):
		build.run(self)

		for base, dirs, files in os.walk(self.build_base):
			for f in files:
				for line in fileinput.input(os.path.join(base, f),inplace=True):
					sys.stdout.write(line.replace('@PACKAGE_VERSION@', package_version))
				for line in fileinput.input(os.path.join(base, f),inplace=True):
					sys.stdout.write(line.replace('@GENTOO_PORTAGE_EPREFIX@', eprefix))


class jc_test(Command):
	user_options = []

	def initialize_options(self):
		self.build_base = None
		self.build_lib = None

	def finalize_options(self):
		self.set_undefined_options('build', ('build_lib', 'build_lib'))

	def run(self):
		self.run_command('build')

		sys.path.insert(0, 'tests')
		sys.path.insert(0, self.build_lib)

		import testsuite
		suite = unittest.defaultTestLoader.loadTestsFromNames(testsuite.__all__, testsuite)

		result = unittest.TextTestRunner().run(suite)
		sys.exit(not result.wasSuccessful())


class jc_install(install):
	"""
	Generate and install the jdk defaults configuration file.

	For the most part useless, wasn't updated in a long time either and doesn't
	reflect reality anymore. Doing it here is at least a lot more maintainable
	then a couple dozen files where it was defined before.
	Also what should be default is a downstream decision and java-config
	shouldn't have any business here. Still keeping it for the time being.
	"""

	def run(self):
		install.run(self)

		arch = os.getenv('ARCH', 'unknown')
		defaults = '*= icedtea'
		if arch in ['amd64', 'x86']:
			defaults = '*= icedtea6 icedtea6-bin icedtea7 icedtea7-bin'
		elif arch in ['ppc-macos', 'x64-macos', 'x86-macos']:
			defaults = '*= apple-jdk-bin'
		elif arch in ['ppc', 'ppc64', 'ppc-linux', 'ppc-aix']:
			defaults = '*= ibm-jdk-bin'
		elif arch in ['arm']:
			defaults = '*= icedtea-7 icedtea-6 icedtea-bin-7 icedtea-bin-6'

		with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
			f.write("# Supported JDKs\n")
			f.write(defaults + "\n")
		confdir = self.root + '/usr/share/java-config-2/config/'
		self.mkpath(confdir)
		self.copy_file(f.name, confdir + 'jdk-defaults.conf', preserve_mode=0)
		os.remove(f.name)

from distutils.core import setup

eprefix = os.getenv('EPREFIX', '')

setup(
	cmdclass = {
		'build' : jc_build,
		'test' : jc_test,
		'install' : jc_install,
	},
	name = 'java-config',
	version = package_version,
	description = 'java enviroment configuration tool',
	long_description = \
	"""
		java-config is a tool for configuring various enviroment
		variables and configuration files involved in the java
		environment for Gentoo Linux.
	""",
	maintainer = 'Gentoo Java Team',
	maintainer_email = 'java@gentoo.org',
	url = 'http://www.gentoo.org',
	packages = ['java_config_2'],
	package_dir = { 'java_config_2' : 'src/java_config_2' },
	scripts = ['src/java-config-2','src/depend-java-query','src/gjl'],
	data_files = [
		(eprefix + '/usr/share/java-config-2/launcher', ['src/launcher.bash']),
		(eprefix + '/usr/share/man/man1/', ['man/java-config-2.1']),
		(eprefix + '/etc/java-config-2/', ['config/virtuals']),
	]
)

# vim: noet:ts=4:
