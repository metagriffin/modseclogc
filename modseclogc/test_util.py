# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.github@metagriffin.net>
# date: 2016/03/18
# copy: (C) Copyright 2016-EOT metagriffin -- see LICENSE.txt
#------------------------------------------------------------------------------
# This software is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#------------------------------------------------------------------------------

import unittest

from . import util

#------------------------------------------------------------------------------
class TestUtil(unittest.TestCase):

  #----------------------------------------------------------------------------
  def test_parseApacheDate(self):
    self.assertEqual(
      util.parseApacheDate('[01/Mar/2016:06:28:51 +0000]'),
      1456813731)
    self.assertEqual(
      util.parseApacheDate('[01/Mar/2016:06:28:51 +0400]'),
      1456799331)
    self.assertEqual(
      util.parseApacheDate('[01/Mar/2016:06:28:51 -0400]'),
      1456828131)

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
