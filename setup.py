#!/usr/bin/env python

from distutils.command.install_scripts import install_scripts
from distutils import log
import os

class my_install_scripts(install_scripts):
	"""Specialized data file install to handle our symlinks"""
	install_scripts.user_options.append(('symlink-tools=', None,
		'List if files to symlink to run-java-tool in script directory'))

	def initialize_options(self):
		install_scripts.initialize_options(self)
		self.symlink_tools = None

	def finalize_options(self):
		install_scripts.finalize_options(self)
		self.ensure_string_list('symlink_tools')
		
	def run(self):
		install_scripts.run(self)
		for tool in self.symlink_tools:
			s = self.install_dir + '/' + tool
			log.info("symbolically linking %s -> %s" % ('run-java-tool',s))
			if not self.dry_run:
				#copy_file is not able to handle relative symlinks with --root
				os.symlink('run-java-tool',s)

from distutils.core import setup
from glob import glob

setup (
	cmdclass={'install_scripts': my_install_scripts},
	name = 'java-config',
	version = '2.1.10',
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
	scripts = ['src/java-config-2','src/depend-java-query','src/run-java-tool', 'src/gjl'],
	data_files = [
		('share/java-config-2/pym/java_config/', glob('src/java_config/*')),
		('share/applications/', ['data/javaws.desktop']),
		('share/mimelnk/application/', ['data/x-java-jnlp-file.desktop']),
		('share/icons/hicolor/48x48/mimetypes/', ['data/application-x-java-jnlp-file.png']),
		('share/pixmaps/', ['data/java-icon48.png']),
		('share/java-config-2/launcher', ['src/launcher.bash']),
		('share/eselect/modules', glob('src/eselect/*.eselect')),
		('/etc/java-config-2/', ['config/virtuals']),
		('/etc/java-config-2/build/', ['config/jdk.conf','config/compilers.conf']),
		('/etc/env.d/',['config/20java-config']),
		('/etc/profile.d/', glob('src/profile.d/*')),
		('/etc/revdep-rebuild/', ['src/revdep-rebuild/60-java'])
	]
)

# vim: noet:ts=4:
