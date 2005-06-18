#!/usr/bin/env python

from distutils.core import setup
import os
import java_config

setup (
	name = 'java-config',
	version = java_config.version,
	description = 'java enviroment configuration tool',
	long_description = \
	"""
		java-config is a tool for configuring various enviroment
		variables and configuration files involved in the java
		enviroment for Gentoo Linux.
	""",
	author = 'Gentoo Java Herd',
	author_email = 'java@gentoo.org',
	packages = ['', 'java_config'],
	package_dir = { '' : os.curdir, 'java_config' : os.curdir + '/java_config' }
)

# vim: noet:ts=4:
