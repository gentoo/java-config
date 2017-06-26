# -*- coding: UTF-8 -*-
# Copyright 2004-2013 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2


class EnvironmentUndefinedError(Exception):
    """The environment variable is undefined."""


class InvalidConfigError(Exception):
    """The configuration file is invalid."""
    def __init__(self, file):
        self.file = file


class InvalidVMError(Exception):
    """The virtual machine does not exist or is invalid."""


class ProviderUnavailableError(Exception):
    """No provider is available for the specified virtual."""

    def __init__( self, virtual, vms, packages ):
        self._virtual = virtual
        self._vms = vms
        self._packages = packages

    def packages(self):
        return self._packages

    def virtual(self):
        return self._virtual

    def vms(self):
        return self._vms

    def __str__(self):
        return """No provider available for %s
Please check your your environment""" % (self._virtual)


class PermissionError(Exception):
    """File permissions are wrong or you are not a privileged user."""


class UnexistingPackageError(Exception):
    """Package does not exist."""
    def __init__(self, package):
        self.package = package

    def __str__(self):
        return "Package %s was not found!" % self.package

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap: