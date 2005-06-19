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
#     April 20, 2005    - Modified Error classes
#                       - Moved to Errors.py

class EnvironmentUndefinedError:
   """
   Environment Variable is undefined!
   """

class RuntimeError:
   """
   General Exception for the java-config utility
   """

class InvalidConfigError:
   """
   Invalid Configuration File
   """
   def __init__(self, file):
      self.file = file 

class InvalidVMError:
   """
   Specified Virtual Machine does not exist or is invalid
   """

class MissingOptionalsError:
   """
   Some optional utilities are missing from a valid VM
   """

class PermissionError:
   """
   The permission on the file are wrong or you are not a privileged user
   """

# vim:set expandtab tabstop=3 shiftwidth=3 softtabstop=3:
