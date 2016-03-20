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

import re

from .part import Part
from .record import Record

#------------------------------------------------------------------------------

parthead_cre = re.compile(
  '^--(?P<id>[a-z0-9]+)-(?P<type>[a-z])--\n$', flags=re.IGNORECASE)

#------------------------------------------------------------------------------
class Source(object):

  #----------------------------------------------------------------------------
  def __init__(self, stream, size, name=None, *args, **kw):
    super(Source, self).__init__(*args, **kw)
    self.stream = stream
    self.name   = name or self.stream.name
    self.size   = size
    self.bytesRead  = 0
    self.linesRead  = 0
    self._next  = []

  #----------------------------------------------------------------------------
  @property
  def remaining(self):
    if self.size is None:
      return None
    return self.size - self.bytesRead

  #----------------------------------------------------------------------------
  def __iter__(self):
    return self

  #----------------------------------------------------------------------------
  def next(self):
    record = None
    while True:
      part = self.getPart()
      if not part:
        if not record:
          raise StopIteration()
        raise ValueError(
          'invalid audit file "%s": no terminating "Z" part' % (self.name,))
      if not record:
        if part.type != 'A':
          raise ValueError(
            'invalid audit file "%s": stand-alone "%s" part'
            % (self.name, part.type))
        record = Record(part.id)
      record.append(part)
      if part.type == 'Z':
        return record

  #----------------------------------------------------------------------------
  def getPart(self):
    lines = []
    while True:
      line = self.getLine()
      if not line:
        if lines:
          return Part(lines[0], lines[1], ''.join(lines[2:]))
        return None
      match = parthead_cre.match(line)
      if match:
        if lines:
          self.putLine(line)
          return Part(lines[0], lines[1], ''.join(lines[2:]))
        lines = [match.group('id'), match.group('type')]
        continue
      lines.append(line)

  #----------------------------------------------------------------------------
  def getLine(self):
    ret = None
    if self._next:
      ret = self._next.pop()
    else:
      ret = self.stream.readline()
    if not ret:
      return ret
    self.linesRead += 1
    self.bytesRead += len(ret)
    return ret

  #----------------------------------------------------------------------------
  def putLine(self, line):
    if self._next:
      raise ValueError('line buffer full')
    self._next.append(line)
    self.bytesRead -= len(line)
    self.linesRead -= 1


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
