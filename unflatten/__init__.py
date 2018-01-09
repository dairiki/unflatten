# -*- coding: utf-8 -*-
""" Unflatten nested dict/array data

"""
from __future__ import absolute_import

from operator import itemgetter
import re

from .compat import string_types


def unflatten(arg):
    """Unflatten nested dict/array data.

    Example::

    >>> unflatten({'foo[0].bar' : 'val'})
    {
        'foo': [
            {'bar': 'val},
            ],
        }


    """
    if hasattr(arg, 'iteritems'):
        items = arg.iteritems()
    elif hasattr(arg, 'items'):
        items = arg.items()
    else:
        items = arg

    data = {}
    holders = []
    for flat_key, val in items:
        parsed_key = _parse_key(flat_key)
        obj = data
        for depth, (key, next_key) in enumerate(zip(parsed_key,
                                                    parsed_key[1:]), 1):
            if isinstance(next_key, string_types):
                holder_type = _dict_holder
            else:
                holder_type = _list_holder

            if key not in obj:
                obj[key] = holder_type(_unparse_key(parsed_key[:depth]))
                holders.append((obj, key))
            elif not isinstance(obj[key], holder_type):
                raise ValueError(
                    "conflicting types %s and %s for key %r" % (
                        _node_type(obj[key]),
                        holder_type.data_type.__name__,
                        _unparse_key(parsed_key[:depth])))
            obj = obj[key]

        last_key = parsed_key[-1]
        if isinstance(obj.get(last_key), _holder):
            raise ValueError(
                "conflicting types %s and terminal for key %r" % (
                    _node_type(obj[last_key]), flat_key))
        obj[last_key] = val

    for obj, key in reversed(holders):
        obj[key] = obj[key].finish()

    return data


def _node_type(value):
    if isinstance(value, _holder):
        return value.data_type.__name__
    else:
        return 'terminal'


class _holder(dict):
    def __init__(self, flat_key):
        self.flat_key = flat_key
        self.data = {}

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]

    def get(self, key):
        return self.data.get(key)

    def __setitem__(self, key, value):
        self.data[key] = value


class _dict_holder(_holder):
    data_type = dict

    def finish(self):
        return self.data


class _list_holder(_holder):
    data_type = list

    def finish(self):
        items = sorted(self.data.items(), key=itemgetter(0))
        value = []
        for n, (key, val) in enumerate(items):
            if key != n:
                assert key > n
                missing_key = "%s[%d]" % (self.flat_key, n)
                raise ValueError("missing key %r" % missing_key)
            value.append(val)
        return value


_INDEX_re = re.compile(r'\[(?P<ind>\d+)\]\Z')


def _parse_key(key):
    if not isinstance(key, string_types):
        raise TypeError("keys must be strings")
    parts = []
    for part in reversed(key.split('.')):
        m = _INDEX_re.search(part)
        while m:
            parts.append(int(m.group('ind')))
            part = part[:m.start()]
            m = _INDEX_re.search(part)
        parts.append(part)
    return tuple(reversed(parts))


def _unparse_key(parsed):
    bits = []
    for part in parsed:
        if isinstance(part, string_types):
            fmt = ".%s" if bits else "%s"
        else:
            fmt = "[%d]"
        bits.append(fmt % part)
    return ''.join(bits)
