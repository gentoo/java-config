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

import os,sys

class OutputFormatter:
   codes = {
               'H': '\x1b[01m',       # Bold
               'U': '\x1b[04m',       # Underline
               'I': '\x1b[07m',       # Inverse
               'b': '\x1b[34;01m',    # Blue
               'B': '\x1b[34;06m',    # Dark Blue
               'c': '\x1b[36;01m',    # Cyan
               'C': '\x1b[36;06m',    # Dark Cyan
               'g': '\x1b[32;01m',    # Green
               'G': '\x1b[32;06m',    # Dark Green
               'm': '\x1b[35;01m',    # Magenta 
               'M': '\x1b[35;06m',    # Dark Magenta
               'r': '\x1b[31;01m',    # Red
               'R': '\x1b[31;06m',    # Dark Red
               'y': '\x1b[33;01m',    # Yellow
               'Y': '\x1b[33;06m',    # Dark Yellow
               '$': '\x1b[0m',        # Reset
               '%': '%'               # Percent
           }
   
   def __init__(self, displayColor=True, displayTitle=True):
      self.colorOutput = displayColor
      self.consoleTitle = displayTitle

      if displayTitle and os.environ.has_key("TERM"):
         if os.environ["TERM"] not in [ "xterm", "Eterm", "aterm", "rxvt" ]:
            self.consoleTitle = False

   def setColorOuputStatus(self, status):
      self.colorOutput = status

   def setDisplayTitleStatus(self, status):
      if status and os.environ.has_key("TERM"):
         if os.environ["TERM"] in [ "xterm", "Eterm", "aterm", "rxvt" ]:
            self.consoleTitle = True
         else:
            self.consoleTitle = False
      else:
         self.consoleTitle = False

   def isColorOutputEnabled(self):
      return self.colorOutput

   def isTitleDisplayEnabled(self):
      return self.consoleTitle


   def __setTitle(self, title):
      if self.displayTitle:
         sys.stderr.write("\x1b]1;\x07\x1b]2;" + str(title) + "\x07")
         sys.stderr.flush()

   def __parseColor(self, message, stripColors=False):
      colored = ''
      striped = ''
      replace = 0

      for char in message:
         if replace:
            colored += self.codes[char]
            if char == '%':
               striped += self.codes[char]
            replace = 0
         elif char == '%':
            replace = 1
         else:
            colored += char
            striped += char

      if stripColors:
         return colored
      else:
         return striped

   def _print(self, message):
      print self.__parseColor(message, self.colorOutput)

   def _printError(self, message):
      message = "%H%R!!! ERROR: " + message + "%$"
      sys.stderr.write(self.__parseColor(message, self.colorOutput) + '\n')

   def _printWarning(self, message):
      message = "%H%Y!!! WARNING: " + message + "%$"
      sys.stderr.write(self.__parseColor(message, self.colorOutput) + '\n')

   def setTitle(self, message):
      self.__setTitle(self.__parseColor(message, True))
