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

class EnvironmentUndefinedError(SystemExit):
   """
   Environment Variable is undefined!
   """

class EnvironmentUnexecutableError(SystemExit):
   """
   The file is not executable!
   """

class RuntimeError(SystemExit):
   """
   General Exception for the java-config utility
   """

class InvalidConfigError:
   """
   Invalid Configuration File
   """
   def __init__(self, file):
      self.file = file 

class InvalidVM:
   """
   Specified Virtual Machine does not exist or is invalid
   """

class MissingOptionals:
   """
   Some optional utilities are missing from a valid VM
   """
