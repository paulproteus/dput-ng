# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# Copyright (c) 2012 dput authors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import os.path

from dput.core import logger
from dput.uploader import AbstractUploader
from dput.exceptions import UploadException
from dput.uploaders.sftp import find_username
from dput.util import run_command


class ScpUploadException(UploadException):
    pass


class ScpUploader(AbstractUploader):
    """
    Provides an interface to upload files through FTP. Supports anonymous
    uploads only for the time being
    """

    def initialize(self, **kwargs):

        login = find_username(self._config)
        self._scp_base = ["scp", "-p", "-C"]
        self._scp_host = "%s@%s" % (login, self._config['fqdn'])
        logger.debug("Using scp to upload to %s" % (self._scp_host))
        logger.warning("SCP is deprecated. Please consider upgrading to SFTP.")

    def upload_file(self, filename):
        basefile = os.path.basename(filename)
        incoming = self._config['incoming']
        targetfile = "%s:%s" % (self._scp_host, os.path.join(incoming,
                                                             basefile))
        scp = self._scp_base + [filename, targetfile]
        #logger.debug("run: %s" % (scp))
        (_, e, x) = run_command(scp)
        if x != 0:
            raise ScpUploadException("Failed to upload %s to %s: %s" % (
                                            basefile, self._config.name(), e))

    def shutdown(self):
        pass