#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011-2013 by Łukasz Langa

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""null
   ----

   Implements the null object pattern."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from collections import MutableMapping, MutableSequence

import six


class _Null(object):
    """See: http://en.wikipedia.org/wiki/Null_Object_pattern"""

    def __init__(self, _unicode="", _repr="Null"):
        self.__dict__['_unicode'] = _unicode
        if six.PY3:
            self.__dict__['_str'] = _unicode
            self.__dict__['_repr'] = _repr
        else:
            self.__dict__['_str'] = _unicode.encode("utf8")
            self.__dict__['_repr'] = _repr.encode("utf8")

    def __unicode__(self):
        return self.__getattribute__("_unicode")

    def __str__(self):
        return self.__getattribute__("_str")

    def __repr__(self):
        return self.__getattribute__("_repr")

    def __nonzero__(self):
        return False

    def __len__(self):
        return 0

    def __getattr__(self, attr):
        return self

    def __setattr__(self, attr, value):
        pass

    def __getitem__(self, item):
        return self

    def __setitem__(self, item, value):
        pass

    def __delitem__(self, item):
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __iter__(self):
        return self

    def next(self):
        raise StopIteration

    __next__ = next


unset = _Null(_unicode="unset", _repr="unset")
Null = _Null()


class NullDict(dict):
    def __missing__(self, key):
        return Null


class NullList(list):
    def __getitem__(self, index):
        if index < len(self):
            return super(NullList, self).__getitem__(index)
        return Null


def nullify(obj):
    if isinstance(obj, MutableMapping):
        d = NullDict()
        for k, v in six.iteritems(obj):
            d[k] = nullify(v)
        return d

    if isinstance(obj, (MutableSequence, tuple)):
        l = NullList()
        for elem in obj:
            l.append(nullify(elem))
        return l

    return obj
