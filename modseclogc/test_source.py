# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.github@metagriffin.net>
# date: 2016/03/19
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

from . import source

#------------------------------------------------------------------------------
class TestSource(unittest.TestCase):

  maxDiff = None

  #----------------------------------------------------------------------------
  def test_source(self):
    stream = six.BytesIO('''\
--7db5817a-A--
[18/Mar/2016:18:39:17 --0400] VuyDlX8AAQEAAG5ffLsAAAAA 127.0.0.1 33184 127.0.0.1 80
--7db5817a-B--
GET /path/to/resource HTTP/1.1
User-Agent: curl/7.35.0
Host: localhost
Accept: */*

--7db5817a-F--
HTTP/1.1 404 Not Found
Content-Length: 288
Content-Type: text/html; charset=iso-8859-1

--7db5817a-E--
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL /path/to/resource was not found on this server.</p>
<hr>
<address>Apache/2.4.7 (Ubuntu) Server at localhost Port 80</address>
</body></html>

--7db5817a-H--
Stopwatch: 1458340757985402 1456 (- - -)
Stopwatch2: 1458340757985402 1456; combined=197, p1=151, p2=35, p3=0, p4=0, p5=11, sr=0, sw=0, l=0, gc=0
Response-Body-Transformed: Dechunked
Producer: ModSecurity for Apache/2.7.7 (http://www.modsecurity.org/).
Server: Apache/2.4.7 (Ubuntu)
Sanitised-Request-Headers: "Authorization".
Engine-Mode: "DETECTION_ONLY"

--7db5817a-Z--
''')
    src = source.Source(stream, size=len(stream.getvalue()), name='<string>')

    self.assertEqual(src.size, 993)
    self.assertEqual(src.remaining, 993)
    records = list(src)
    self.assertEqual(src.size, 993)
    self.assertEqual(src.linesRead, 34)
    self.assertEqual(src.remaining, 0)
    self.assertEqual(len(records), 1)

    rec = records[0]
    self.assertEqual(rec.id, '7db5817a')
    out = six.BytesIO()
    rec.renderNative(out)
    self.assertMultiLineEqual(out.getvalue(), '''\
--7db5817a-A--
[18/Mar/2016:18:39:17 --0400] VuyDlX8AAQEAAG5ffLsAAAAA 127.0.0.1 33184 127.0.0.1 80
--7db5817a-B--
GET /path/to/resource HTTP/1.1
User-Agent: curl/7.35.0
Host: localhost
Accept: */*

--7db5817a-F--
HTTP/1.1 404 Not Found
Content-Length: 288
Content-Type: text/html; charset=iso-8859-1

--7db5817a-E--
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL /path/to/resource was not found on this server.</p>
<hr>
<address>Apache/2.4.7 (Ubuntu) Server at localhost Port 80</address>
</body></html>

--7db5817a-H--
Stopwatch: 1458340757985402 1456 (- - -)
Stopwatch2: 1458340757985402 1456; combined=197, p1=151, p2=35, p3=0, p4=0, p5=11, sr=0, sw=0, l=0, gc=0
Response-Body-Transformed: Dechunked
Producer: ModSecurity for Apache/2.7.7 (http://www.modsecurity.org/).
Server: Apache/2.4.7 (Ubuntu)
Sanitised-Request-Headers: "Authorization".
Engine-Mode: "DETECTION_ONLY"

--7db5817a-Z--

''')


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
