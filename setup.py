#!/usr/bin/env python

from distutils.core import setup
import os

setup (
	name = 'java-config',
	version = '2.0.3',
	description = 'java enviroment configuration tool',
	long_description = \
	"""
		java-config is a tool for configuring various enviroment
		variables and configuration files involved in the java
		enviroment for Gentoo Linux.
	""",
	maintainer = 'Gentoo Java Herd',
	maintainer_email = 'java@gentoo.org',
	url = 'http://www.gentoo.org',
	packages = ['java_config'],
	package_dir = { 'java_config' : 'src/java_config' },
	scripts = ['src/java-config','src/depend-java-query','src/run-java-tool', 'src/gjl'],
	data_files = [
		('man/man1', ['man/java-config.1']),
		('share/java-config/config', ['config/jdk-defaults.conf']),
		('share/java-config/launcher', ['src/launcher.bash']),
		('/etc/java-config/', ['config/jdk.conf','config/symlink-tools']),
		('/etc/java-config/vms', ['src/env']),
		('/etc/env.d/',['config/20java-config']),
	]
)

# vim: noet:ts=4:
