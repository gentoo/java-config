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

class JavaConfig_RuntimeError(SystemExit):
   """
   General Exception for the java-config utility
   """
