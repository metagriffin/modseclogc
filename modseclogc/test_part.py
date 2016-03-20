# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.github@metagriffin.net>
# date: 2016/03/17
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
import six

from . import part

#------------------------------------------------------------------------------
class TestPart(unittest.TestCase):

  #----------------------------------------------------------------------------
  def test_factory(self):
    prt = part.Part('1234', 'A', '...')
    self.assertIsInstance(prt, part.Part)
    self.assertIsInstance(prt, part.PartA)
    self.assertIs(type(prt), part.PartA)
    prt = part.Part('1234', 'NoSuchPartType', '...')
    self.assertIsInstance(prt, part.Part)
    self.assertIs(type(prt), part.Part)

  #----------------------------------------------------------------------------
  def test_part_a(self):
    out = six.BytesIO()
    pa  = part.Part(
      '12345',
      'A',
      '[01/Mar/2016:06:28:51 +0000] VtU2o38AAQEAAEV6AuwAAAAE 10.10.10.1 34882 127.0.0.1 80\n'
    )
    self.assertEqual(pa.id, '12345')
    self.assertEqual(pa.type, 'A')
    self.assertEqual(pa.timestamp, 1456813731)
    self.assertEqual(pa.unique_id, 'VtU2o38AAQEAAEV6AuwAAAAE')
    self.assertEqual(pa.client_ip, '10.10.10.1')
    self.assertEqual(pa.client_port, 34882)
    self.assertEqual(pa.server_ip, '127.0.0.1')
    self.assertEqual(pa.server_port, 80)
    pa.renderNative(out)
    self.assertEqual(
      out.getvalue(),
      '''\
--12345-A--
[01/Mar/2016:06:28:51 +0000] VtU2o38AAQEAAEV6AuwAAAAE 10.10.10.1 34882 127.0.0.1 80
''')

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
