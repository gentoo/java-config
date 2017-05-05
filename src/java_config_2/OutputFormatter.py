# -*- coding: UTF-8 -*-
# Copyright 2004-2013 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

import sys
import os

class OutputFormatter:
    codes = {
              'H': '\x1b[01m',        # Bold
              'U': '\x1b[04m',        # Underline
              'I': '\x1b[07m',        # Inverse
              'b': '\x1b[34;01m',     # Blue
              'B': '\x1b[34;06m',     # Dark Blue
              'c': '\x1b[36;01m',     # Cyan
              'C': '\x1b[36;06m',     # Dark Cyan
              'g': '\x1b[32;01m',     # Green
              'G': '\x1b[32;06m',     # Dark Green
              'm': '\x1b[35;01m',     # Magenta
              'M': '\x1b[35;06m',     # Dark Magenta
              'r': '\x1b[31;01m',     # Red
              'R': '\x1b[31;06m',     # Dark Red
              'y': '\x1b[33;01m',     # Yellow
              'Y': '\x1b[33;06m',     # Dark Yellow
              '$': '\x1b[0m',         # Reset
              '%': '%'                # Percent
             }

    def __init__(self, displayColor=True, displayTitle=True, autoIndent=True):
        self.colorOutput = displayColor
        self.autoIndent = autoIndent

    def __call__(self, displayColor=True, displayTitle=True, autoIndent=True):
        return self

    def setColorOutputStatus(self, status):
        self.colorOutput = status

    def __indent(self, prefix, message):
        if self.autoIndent is True:
            num = len(prefix)
            return prefix + message.replace('\n', '\n'+' '*num)

        else:
            return prefix + message

    def __parseColor(self, message):
        colored = ''
        striped = ''
        replace = 0

        for char in str(message):
            if replace:
                if char == ' ':
                    colored += self.codes['%'] + ' '
                    striped += self.codes['%'] + ' '
                elif char == '%':
                    colored += self.codes[char]
                    striped += self.codes[char]
                else:
                    colored += self.codes[char]
                replace = 0
            elif char == '%':
                replace = 1
            else:
                colored += char
                striped += char

        if self.colorOutput:
            return colored
        else:
            return striped

    def write(self, message):
        print(self.__parseColor(message.strip()))

    def _print(self, message):
        print(self.__parseColor(message))

    def _printError(self, message):
        message = "%H%R" + self.__indent("!!! ERROR: ", message) + "%$"
        sys.stderr.write(self.__parseColor(message) + '\n')

    def _printWarning(self, message):
        message = "%H%Y" + self.__indent("!!! WARNING: ", message) + "%$"
        sys.stderr.write(self.__parseColor(message) + '\n')

    def _printAlert(self, message):
        message = "%H%C" + self.__indent("!!! ALERT: ", message) +  "%$"
        sys.stderr.write(self.__parseColor(message) + '\n')


OutputFormatter = OutputFormatter()
# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
