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

from datetime import datetime
import calendar

# todo: do i really need `pytz`?...
import pytz

#------------------------------------------------------------------------------
def parseApacheDate(date):
  if not date.startswith('[') or not date.endswith(']'):
    raise ValueError('invalid apache log date: %r' % (date,))
  date = date[1:-1]
  ts = datetime.strptime(date.split()[0], '%d/%b/%Y:%H:%M:%S')
  ts.replace(tzinfo=pytz.UTC)
  ts = calendar.timegm(ts.utctimetuple())
  offset = ( int(date[-5:-2]) * 60 + int(date[-2:]) ) * 60
  return ts - offset
    

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
