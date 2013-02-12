#!/usr/bin/env python

#######################################
package_version = '2.2.0'
#######################################

from distutils.command.build import build
from distutils.command.install import install
import fileinput, os, sys

class my_build(build):

	def run(self):
		build.run(self)

		eprefix = os.getenv('EPREFIX', '')
		for base, dirs, files in os.walk(self.build_base):
			for f in files:
				for line in fileinput.input(os.path.join(base, f),inplace=True):
					sys.stdout.write(line.replace('@PACKAGE_VERSION@', package_version))
				for line in fileinput.input(os.path.join(base, f),inplace=True):
					sys.stdout.write(line.replace('@GENTOO_PORTAGE_EPREFIX@', eprefix))


class my_install(install):
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
			defaults = '*= icedtea6 icedtea6-bin sun-jdk blackdown-jdk ibm-jdk-bin jrockit-jdk-bin'
		elif arch in ['ppc-macos', 'x64-macos', 'x86-macos']:
			defaults = '*= apple-jdk-bin'
		elif arch in ['amd64-fbsd', 'x86-fbsd', 'x64-freebsd', 'x86-freebsd']:
			defaults = '*= diablo-jdk'
		elif arch in ['sparc-solaris', 'sparc64-solaris', 'x64-solaris', 'x86-solaris']:
			defaults = '*= sun-jdk'
		elif arch in ['mips', 'sparc']:
			defaults = '*= blackdown-jdk'
		elif arch in ['ppc', 'ppc64', 'ppc-linux', 'ppc-aix']:
			defaults = '*= ibm-jdk-bin'
		elif arch in ['alpha']:
			defaults = '*= compaq-jdk'
		elif arch in ['arm']:
			defaults = '*= icedtea-7 icedtea-6 icedtea-bin-7 icedtea-bin-6'
		elif arch in ['ia64']:
			defaults = '*= jrockit-jdk-bin'
		elif arch in ['hppa']:
			defaults = '*= kaffe'
		elif arch in ['hpux']:
			defaults = '*= hp-jdk-bin'

		os.mkdir(self.root + '/usr/share/java-config-2/config/')
		with open(self.root + '/usr/share/java-config-2/config/jdk-defaults.conf', 'w') as f:
			f.write("# This files contain the default support jdk's\n")
			f.write(defaults + "\n")


from distutils.core import setup

setup (
	cmdclass={'build' : my_build, 'install' : my_install},
	name = 'java-config',
	version = package_version,
	description = 'java enviroment configuration tool',
	long_description = \
	"""
		java-config is a tool for configuring various enviroment
		variables and configuration files involved in the java
		enviroment for Gentoo Linux.
	""",
	maintainer = 'Gentoo Java Team',
	maintainer_email = 'java@gentoo.org',
	url = 'http://www.gentoo.org',
	packages = ['java_config_2'],
	package_dir = { 'java_config_2' : 'src/java_config_2' },
	scripts = ['src/java-config-2','src/depend-java-query','src/gjl'],
	data_files = [
		('share/java-config-2/launcher', ['src/launcher.bash']),
		('/etc/java-config-2/', ['config/virtuals']),
		('/etc/java-config-2/build/', ['config/jdk.conf','config/compilers.conf']),
	]
)

# vim: noet:ts=4:
