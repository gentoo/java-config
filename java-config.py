#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2004 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

# Author: Saleem Abdulrasool <compnerd@compnerd.org>
# Maintainer: Gentoo Java Herd <java@gentoo.org>
# Java Subsystem Configuration Utility for Gentoo Linux

# ChangeLog
# Saleem A. <compnerd@compnerd.org>
#     December 30, 2004 - Initial Rewrite
#                       - Based on the collective works of the following:
#                         {karltk,axxo,aether}@gentoo.org

__version__ = '$Revision: 2.0$'[11:-1]

import OutputFormatter,EnvironmentManager 

from optparse import OptionParser, make_option

if __name__ == '__main__':
   usage = "java-config [options]\n\n"
   usage += "Java Configuration Utility Version " + str(__version__) + "\n"
   usage += "Copyright 2004 Gentoo Foundation\n"
   usage += "Distributed under the terms of the GNU General Public License v2\n"
   usage += "Please contact the Gentoo Java Herd <java@gentoo.org> with problems."

   options_list = [
                     make_option ("-v", "--version", action="store_true",  default=False, dest="optVersion",   help="Print version information"),
                     make_option ("-n", "--nocolor", action="store_false", default=True, dest="optColor",     help="Disable color output"),
                     make_option ("-J", "--java",    action="store_true",  default=False, dest="optJavaExec",  help="Print the location of the java executable"),
                     make_option ("-c", "--javac",   action="store_true",  default=False, dest="optJavacExec", help="Print the location of the javac executable")
                  ]

   parser = OptionParser(usage, options_list)
   (options, args) = parser.parse_args()

   printer = OutputFormatter.OutputFormatter(options.optColor, True)
   manager = EnvironmentManager.EnvironmentManager()

   if options.optVersion:
      printer._print("%H%BJava Configuration Utility %GVersion " + str(__version__))
      raise SystemExit()
