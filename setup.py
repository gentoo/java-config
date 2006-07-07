#!/usr/bin/env python

from distutils.core import setup
import os
from os import listdir

setup (
	name = 'java-config',
	version = '2.0.27',
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
	#packages = ['java_config'],
	#package_dir = { 'java_config' : 'src/java_config' },
	scripts = ['src/java-config-2','src/depend-java-query','src/run-java-tool', 'src/gjl'],
	data_files = [
		('share/java-config-2/pym/java_config/', ['src/java_config/'+file for file in listdir('src/java_config/')] ),
		('share/man/man1', ['man/java-config-2.1']),
		('share/java-config-2/launcher', ['src/launcher.bash']),
		('share/eselect/modules', ['src/eselect/java-vm.eselect','src/eselect/java-nsplugin.eselect']),
		('/etc/java-config-2/', ['config/virtuals']),
		('/etc/java-config-2/build/', ['config/jdk.conf','config/compilers.conf']),
		('/etc/env.d/',['config/20java-config']),
	]
)

# vim: noet:ts=4:
