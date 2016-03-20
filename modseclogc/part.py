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

from . import util

#------------------------------------------------------------------------------
class Part(object):

  AUDIT_HEADER                                      = 'A'
  REQUEST_HEADERS                                   = 'B'
  REQUEST_BODY                                      = 'C'
  INTENDED_RESPONSE_HEADERS                         = 'D'
  INTENDED_RESPONSE_BODY                            = 'E'
  RESPONSE_HEADERS                                  = 'F'
  RESPONSE_BODY                                     = 'G'
  AUDIT_TRAILER                                     = 'H'
  REDUCED_MULTIPART_REQUEST_BODY                    = 'I'
  MULTIPART_FILES_INFORMATION                       = 'J'
  MATCHED_RULES_INFORMATION                         = 'K'
  AUDIT_FOOTER                                      = 'Z'

  #----------------------------------------------------------------------------
  def __new__(cls, id, type, *args, **kw):
    if cls is not Part:
      return super(Part, cls).__new__(cls, id, type, *args, **kw)
    try:
      target = eval('Part' + type)
    except NameError:
      target = Part
    if target is Part:
      return super(Part, cls).__new__(cls, id, type, *args, **kw)
    return target(id, type, *args, **kw)

  #----------------------------------------------------------------------------
  def __init__(self, id, type, body, *args, **kw):
    super(Part, self).__init__(*args, **kw)
    self.id   = id
    self.type = type
    self.body = body

  #----------------------------------------------------------------------------
  def renderNative(self, output):
    output.write('--%s-%s--\n' % (self.id, self.type))
    output.write(self.body)


#------------------------------------------------------------------------------
class PartA(Part):

  #----------------------------------------------------------------------------
  @property
  def timestamp(self):
    return util.parseApacheDate(' '.join(self.body.split(' ', 2)[0:2]))

  #----------------------------------------------------------------------------
  @property
  def unique_id(self):
    return self.body.split(' ', 3)[2]

  #----------------------------------------------------------------------------
  @property
  def client_ip(self):
    return self.body.split(' ', 4)[3]

  #----------------------------------------------------------------------------
  @property
  def client_port(self):
    return int(self.body.split(' ', 5)[4])

  #----------------------------------------------------------------------------
  @property
  def server_ip(self):
    return self.body.split(' ', 6)[5]

  #----------------------------------------------------------------------------
  @property
  def server_port(self):
    return int(self.body.split(' ', 7)[6])


#------------------------------------------------------------------------------
class PartZ(Part):

  #----------------------------------------------------------------------------
  def __init__(self, *args, **kw):
    super(PartZ, self).__init__(*args, **kw)
    self.body = '\n'


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
