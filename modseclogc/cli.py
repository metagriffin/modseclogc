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

import sys
import argparse

from . import engine
from . import matcher
from . import renderer
from . import source
from .i18n import _

#------------------------------------------------------------------------------
def main(argv=None):
  cli = argparse.ArgumentParser(
    # usage='%(prog)s [options] [FILENAME | "-"]',
    description=_(
      'Manipulates ModSecurity audit log files'
      ' -- see https://github.com/metagriffin/modseclogc'),
    # epilog='%(prog)s ' + lib.version,
  )

  #-------------------------------------
  # which records to match

  # cli.add_argument(
  #   _('--match'), metavar=_('EXPR'),
  #   dest='match', default=None,
  #   help=_('matching expression using the modseclogc expression language'))

  cli.add_argument(
    _('--match-id'), metavar=_('UNIQUE_ID'),
    dest='match_id', default=None,
    help=_('request unique ID to match'))

  cli.add_argument(
    _('--match-path'), metavar=_('GLOB'),
    dest='match_path', default=None,
    help=_('request path (as a glob pattern) to match'))

  cli.add_argument(
    _('--match-method'), metavar=_('METHOD'),
    dest='match_method', default=None,
    help=_('comma-separated list of request methods to match'
           ' (e.g. "GET", "PUT", etc.)'))

  cli.add_argument(
    _('--match-nth'), metavar=_('NTH[-MTH]'),
    dest='match_nth', default=None,
    help=_('match the nth through mth request by one-based index'))

  #-------------------------------------
  # how to render matched records

  cli.add_argument(
    _('--show-id'),
    dest='show_id', action='store_true', default=False,
    help=_('show the request unique ID'))

  cli.add_argument(
    _('--show-request-line'),
    dest='show_request_line', action='store_true', default=False,
    help=_('show the "request line"'))

  cli.add_argument(
    _('--show-part-list'),
    dest='show_part_list', action='store_true', default=False,
    help=_('list all the available parts per record'))

  cli.add_argument(
    _('--show-parts'),
    dest='show_parts', default=None,
    help=_('show only the specified audit parts; e.g. "ABZ"'))

  cli.add_argument(
    _('--hide-parts'),
    dest='hide_parts', default=None,
    help=_('hide the specified audit parts; e.g. "C"'))

  cli.add_argument(
    _('--unmatched'), metavar=_('ACTION'),
    dest='unmatched', default='drop',
    help=_('how to render unmatched records (one of "drop" or "keep")'))

  #-------------------------------------
  # where to get records from

  cli.add_argument(
    'filename', metavar=_('FILENAME'),
    nargs='?',
    help=_('filename to parse; if not specified or "-", STDIN'
           ' is used instead'))

  options = cli.parse_args(argv)

  # TODO: detect option collisions (most rendering options are
  #       mutually exclusive)

  match = matcher.AndMatcher()

  if options.match_id:
    match.append(matcher.IdMatcher(options.match_id))
  if options.match_path:
    match.append(matcher.PathMatcher(options.match_path))
  if options.match_method:
    match.append(matcher.MethodMatcher(options.match_method))
  if options.match_nth:
    match.append(matcher.NthMatcher(options.match_nth))
  # if options.match:
  #   match.append(matcher.ExpressionMatcher(options.match))

  hitrender = renderer.SerialRenderer()

  if options.show_id:
    hitrender.append(renderer.IdRenderer())
  if options.show_request_line:
    hitrender.append(renderer.RequestLineRenderer())
  if options.show_part_list:
    hitrender.append(renderer.PartListRenderer())
  if options.show_parts:
    hitrender.append(renderer.ShowPartsRenderer(options.show_parts))
  if options.hide_parts:
    hitrender.append(renderer.HidePartsRenderer(options.hide_parts))

  if not hitrender.count > 0:
    hitrender = None

  missrender = None
  if options.unmatched == 'keep':
    missrender = renderer.NativeRenderer()

  alwaysrender = None
  # TODO: `always` (progress indicator)

  eng = engine.Engine(
    match  = match,
    hit    = hitrender,
    miss   = missrender,
    always = alwaysrender,
  )

  if options.filename and options.filename[0] != '-':
    # TODO: multi-file, size, name, ...
    fname = options.filename[0]
    src = source.Source(open(fname, 'rb'), size=None, name=fname)
  else:
    src = source.Source(sys.stdin, size=None, name='<stdin>')

  dst = sys.stdout

  eng.process(src, dst)

#------------------------------------------------------------------------------
if __name__ == '__main__':
  sys.exit(main(sys.argv))

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
