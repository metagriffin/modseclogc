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

from collections import OrderedDict

from .part import Part

#------------------------------------------------------------------------------
class Renderer(object):

  #----------------------------------------------------------------------------
  def __init__(self, *args, **kw):
    super(Renderer, self).__init__(*args, **kw)

  #----------------------------------------------------------------------------
  def render(self, record, output):
    raise NotImplementedError()


#------------------------------------------------------------------------------
class NullRenderer(Renderer):
  def render(self, record, output):
    pass


#------------------------------------------------------------------------------
class SerialRenderer(Renderer):

  #----------------------------------------------------------------------------
  def __init__(self, *args, **kw):
    super(SerialRenderer, self).__init__(*args, **kw)
    self.renderers = []

  #----------------------------------------------------------------------------
  def append(self, renderer):
    self.renderers.append(renderer)

  #----------------------------------------------------------------------------
  @property
  def count(self):
    return len(self.renderers)

  #----------------------------------------------------------------------------
  def render(self, record, output):
    for sub in self.renderers:
      sub.render(record, output)


#------------------------------------------------------------------------------
class NativeRenderer(Renderer):
  def render(self, record, output):
    record.renderNative(output)


#------------------------------------------------------------------------------
class IdRenderer(Renderer):
  def render(self, record, output):
    output.write(record.parts[Part.AUDIT_HEADER].unique_id)
    output.write('\n')


#------------------------------------------------------------------------------
class RequestLineRenderer(Renderer):
  def render(self, record, output):
    if Part.REQUEST_HEADERS in record.parts:
      output.write(record.parts[Part.REQUEST_HEADERS].body.split('\n')[0])
      output.write('\n')


#------------------------------------------------------------------------------
class PartListRenderer(Renderer):
  def render(self, record, output):
    output.write(''.join(record.parts.keys()))
    output.write('\n')


#------------------------------------------------------------------------------
class ShowPartsRenderer(Renderer):

  #----------------------------------------------------------------------------
  def __init__(self, parts, *args, **kw):
    super(ShowPartsRenderer, self).__init__(*args, **kw)
    self.parts = parts
    self.show = True

  #----------------------------------------------------------------------------
  def render(self, record, output):
    sel = OrderedDict([(k, v) for k, v in record.parts.items()])
    if self.show:
      for part in list(sel.keys()):
        if part not in self.parts:
          sel.pop(part, None)
    else:
      for part in self.parts:
        sel.pop(part, None)
    for part in sel.values():
      part.renderNative(output)


#------------------------------------------------------------------------------
class HidePartsRenderer(ShowPartsRenderer):
  def __init__(self, *args, **kw):
    super(HidePartsRenderer, self).__init__(*args, **kw)
    self.show = False


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
