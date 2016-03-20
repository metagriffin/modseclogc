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

import globre

from .part import Part

#------------------------------------------------------------------------------
class Matcher(object):

  #----------------------------------------------------------------------------
  def __init__(self, *args, **kw):
    super(Matcher, self).__init__(*args, **kw)

  #----------------------------------------------------------------------------
  def match(self, record):
    raise NotImplementedError()

  ## def __not__ ...


#------------------------------------------------------------------------------
class TrueMatcher(object):
  def match(self, record):
    return True


#------------------------------------------------------------------------------
class FalseMatcher(object):
  def match(self, record):
    return False


#------------------------------------------------------------------------------
class InverseMatcher(Matcher):
  def __init__(self, matcher, *args, **kw):
    super(InverseMatcher, self).__init__(*args, **kw)
    self.matcher = matcher
  def match(self, record):
    return not self.matcher.match(record)


#------------------------------------------------------------------------------
class AndMatcher(Matcher):

  #----------------------------------------------------------------------------
  def __init__(self, *args, **kw):
    super(AndMatcher, self).__init__(*args, **kw)
    self.matchers = []

  #----------------------------------------------------------------------------
  def append(self, matcher):
    self.matchers.append(matcher)

  #----------------------------------------------------------------------------
  @property
  def count(self):
    return len(self.matchers)

  #----------------------------------------------------------------------------
  def match(self, record):
    for sub in self.matchers:
      if not sub.match(record):
        return False
    return True


#------------------------------------------------------------------------------
class IdMatcher(Matcher):
  def __init__(self, id, *args, **kw):
    super(IdMatcher, self).__init__(*args, **kw)
    self.id = id
  def match(self, record):
    return record.parts['A'].unique_id == self.id


#------------------------------------------------------------------------------
class NthMatcher(Matcher):
  cre = re.compile('^(?P<min>\\d+)(-(?P<max>\\d+))?$')
  def __init__(self, expr, *args, **kw):
    super(NthMatcher, self).__init__(*args, **kw)
    self.index = 0
    match = self.cre.match(expr)
    if not match:
      raise ValueError('invalid nth expression: %r' % (expr,))
    self.min = int(match.group('min'))
    self.max = int(match.group('max') or self.min)
    if self.min > self.max:
      raise ValueError('invalid nth expression: %r' % (expr,))
  def match(self, record):
    self.index += 1
    if self.index < self.min or self.index > self.max:
      return False
    return True


#------------------------------------------------------------------------------
class PathMatcher(Matcher):

  #----------------------------------------------------------------------------
  def __init__(self, path, *args, **kw):
    super(PathMatcher, self).__init__(*args, **kw)
    self.path = globre.compile(path, flags=globre.EXACT)

  #----------------------------------------------------------------------------
  def match(self, record):
    if Part.REQUEST_HEADERS not in record.parts:
      return False
    segs = record.parts[Part.REQUEST_HEADERS].body.split('\n')[0].split()
    if len(segs) != 3:
      return False
    path = segs[1]
    if '?' in path:
      path = path.split('?', 1)[0]
    return bool(self.path.match(path))


#------------------------------------------------------------------------------
class MethodMatcher(Matcher):

  #----------------------------------------------------------------------------
  def __init__(self, methods, *args, **kw):
    super(MethodMatcher, self).__init__(*args, **kw)
    self.methods = methods.upper().split(',')

  #----------------------------------------------------------------------------
  def match(self, record):
    if Part.REQUEST_HEADERS not in record.parts:
      return False
    segs = record.parts[Part.REQUEST_HEADERS].body.split('\n')[0].split()
    if len(segs) != 3:
      return False
    method = segs[0].upper()
    return method in self.methods


# #------------------------------------------------------------------------------
# class CookieMatcher(Matcher):
#   def __init__(self, cookie, *args, **kw):
#     super(CookieMatcher, self).__init__(*args, **kw)
#     self.cookie = cookie
#   def match(self, record):
#     # TODO: implement...
#     return False


# #------------------------------------------------------------------------------
# class ExpressionMatcher(Matcher):
#   def __init__(self, expr, *args, **kw):
#     super(ExpressionMatcher, self).__init__(*args, **kw)
#     self.expr = expr
#     TODO: pull these names from plugin specs...
#     def id(val): ...
#     def path(val): ...
#     def cookie(val): ...
#     ...
#   def match(self, record):
#     ...
#     ...


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
