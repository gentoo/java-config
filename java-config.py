#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2004 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

# Author: Saleem Abdulrasool <compnerd@gentoo.org>
# Maintainer: Gentoo Java Herd <java@gentoo.org>
# Java Subsystem Configuration Utility for Gentoo Linux

# ChangeLog
# Saleem A. <compnerd@gentoo.org>
#     December 30, 2004 - Initial Rewrite
#                       - Based on the collective works of the following:
#                         {karltk,axxo,aether}@gentoo.org

__version__ = '$Revision: 2.0$'[11:-1]

import OutputFormatter,EnvironmentManager,JavaExceptions

from optparse import OptionParser, make_option

if __name__ == '__main__':
   usage = "java-config [options]\n\n"
   usage += "Java Configuration Utility Version " + str(__version__) + "\n"
   usage += "Copyright 2004 Gentoo Foundation\n"
   usage += "Distributed under the terms of the GNU General Public License v2\n"
   usage += "Please contact the Gentoo Java Herd <java@gentoo.org> with problems."

   options_list = [
                     make_option ("-v", "--version",  action="store_true",  default=False, dest="optVersion",   help="Print version information"),
                     make_option ("-n", "--nocolor",  action="store_false", default=True,  dest="optColor",     help="Disable color output"),
                     make_option ("-J", "--java",     action="store_true",  default=False, dest="optJavaExec",  help="Print the location of the java executable"),
                     make_option ("-c", "--javac",    action="store_true",  default=False, dest="optJavacExec", help="Print the location of the javac executable"),
                     make_option ("-j", "--jar",      action="store_true",  default=False, dest="optJarExec",   help="Print the location of the jar executable"),
                     make_option ("-O", "--jdk-home", action="store_true",  default=False, dest="optJDKHome",   help="Print the location of the active JDK home"),
                     make_option ("-o", "--jre-home", action="store_true",  default=False, dest="optJREHome",   help="Print the location of the active JRE home")
                  ]

   parser = OptionParser(usage, options_list)
   (options, args) = parser.parse_args()

   printer = OutputFormatter.OutputFormatter(options.optColor, True)

   try:
      manager = EnvironmentManager.EnvironmentManager()
   except JavaExceptions.EnvironmentUndefinedError:
      printer._printError("%RError: %HNo JAVA_HOME available! Please set your Java Virtual Machine")
      sys.exit(-1)
      
   if options.optVersion:
      printer._print("%H%BJava Configuration Utility %GVersion " + str(__version__))
      raise SystemExit()

   if options.optJavaExec:
      try:
         printer._print(manager.find_exec('java'))
      except JavaExceptions.EnvironmentUnexecutableError:
         printer._printError("%RError: %HThe java executable was not found in the Java Path")

   if options.optJavacExec:
      try:
         printer._print(manager.find_exec('javac'))
      except JavaExceptions.EnvironmentUnexecutableError:
         printer._printError("%RError: %HThe javac executable was not found in the Java Path")

   if options.optJarExec:
      try:
         printer._print(manager.find_exec('jar'))
      except JavaExceptions.EnvironmentUnexecutableError:
         printer._printError("%RError: %HThe jar executable was not found in the Java Path")

   if options.optJDKHome:
      try:
         printer._print(manager.query_variable('JDK_HOME'))
      except JavaExceptions.EnvironmentUndefinedError:
         print

   if options.optJREHome:
      try:
         printer._print(manager.query_variable('JRE_HOME'))
      except JavaExceptions.EnvironmentUndefinedError:
         print
