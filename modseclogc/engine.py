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

from . import renderer
from . import matcher

#------------------------------------------------------------------------------
class Engine(object):

  #----------------------------------------------------------------------------
  def __init__(self, match=None, hit=None, miss=None, always=None, *args, **kw):
    super(Engine, self).__init__(*args, **kw)
    self.matcher  = match  or matcher.TrueMatcher()
    self.hit      = hit    or renderer.NativeRenderer()
    self.miss     = miss   or renderer.NullRenderer()
    self.always   = always or renderer.NullRenderer()

  #----------------------------------------------------------------------------
  def process(self, source, output):
    for record in source:
      if self.matcher.match(record):
        self.hit.render(record, output)
      else:
        self.miss.render(record, output)
      self.always.render(record, output)


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
