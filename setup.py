#!/usr/bin/env python

from distutils.command.build import build
import fileinput, os, sys

class my_build(build):

	def run(self):
		build.run(self)

		eprefix = os.getenv('EPREFIX', '')
		for base, dirs, files in os.walk(self.build_base):
			for f in files:
				for line in fileinput.input(os.path.join(base, f),inplace=True):
					sys.stdout.write(line.replace('@GENTOO_PORTAGE_EPREFIX@', eprefix))


from distutils.core import setup

setup (
	cmdclass={'build' : my_build},
	name = 'java-config',
	version = '2.1.12',
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
