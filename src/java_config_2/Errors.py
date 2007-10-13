# -*- coding: UTF-8 -*-

# Copyright 2004-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

class EnvironmentUndefinedError(Exception):
    """
    Environment Variable is undefined!
    """

class InvalidConfigError(Exception):
    """
    Invalid Configuration File
    """
    def __init__(self, file):
        self.file = file 

class InvalidVMError(Exception):
    """
    Specified Virtual Machine does not exist or is invalid
    """

class ProviderUnavailableError(Exception):
    """
    No provider is available for the specified Virtual.
    """

    def __init__( self, virtual, vms, packages ):
        self.virtual = virtual
        self.vms = vms
        self.packages = packages

class MissingOptionalsError(Exception):
    """
    Some optional utilities are missing from a valid VM
    """

class PermissionError(Exception):
    """
    The permission on the file are wrong or you are not a privileged user
    """

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
