# -*- coding: utf-8 -*-
""" Unflatten nested dict/array data

"""
from __future__ import absolute_import

from operator import itemgetter
import re
import sys

if sys.version_info[0] == 2:
    string_type = basestring    # noqa: F821
else:
    string_type = str


def unflatten(arg):
    """Unflatten nested dict/array data.

    This function takes a single argument which may either be a
    ``dict`` (or any object having a dict-like ``.items()`` or
    ``.iteritems()`` method) or a sequence of ``(key, value)`` pairs.
    The keys in the ``dict`` or sequence should must all be strings.

    Examples
    --------

    Nested ``dict``\\s::

    >>> unflatten({'foo.bar': 'val'})
    {'foo': {'bar': 'val'}}

    Nested ``list``::

    >>> unflatten({'foo[0]': 'val', 'foo[1]': 'bar'})
    {'foo': ['val', 'bar']}

    Nested ``list``\\s::

    >>> unflatten({'foo[0][0]': 'val'})
    {'foo': [['val']]}

    Lists of ``dict``\\s::

    >>> unflatten({'foo[0].bar': 'val',
    ...            'foo[1].baz': 'x'})
    {'foo': [{'bar': 'val'}, {'baz': 'x'}]}

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
            if isinstance(next_key, string_type):
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
                        holder_type.node_type,
                        _unparse_key(parsed_key[:depth])))
            obj = obj[key]

        last_key = parsed_key[-1]
        if isinstance(obj.get(last_key), _holder):
            raise ValueError(
                "conflicting types %s and terminal for key %r" % (
                    _node_type(obj[last_key]), flat_key))
        obj[last_key] = val

    for obj, key in reversed(holders):
        obj[key] = obj[key].getvalue()

    return data


def _node_type(value):
    if isinstance(value, _holder):
        return value.node_type,
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
    node_type = dict

    def getvalue(self):
        return self.data


class _list_holder(_holder):
    node_type = list

    def getvalue(self):
        items = sorted(self.data.items(), key=itemgetter(0))
        value = []
        for n, (key, val) in enumerate(items):
            if key != n:
                assert key > n
                missing_key = "%s[%d]" % (self.flat_key, n)
                raise ValueError("missing key %r" % missing_key)
            value.append(val)
        return value


_dot_or_indexes_re = re.compile(r'(\.|(?:\[\d+\])+(?=\.|\Z))')


def _parse_key(flat_key):
    if not isinstance(flat_key, string_type):
        raise TypeError("keys must be strings")

    split_key = _dot_or_indexes_re.split(flat_key)
    parts = [split_key[0]]
    for i in range(1, len(split_key), 2):
        sep = split_key[i]
        if sep == '.':
            parts.append(split_key[i + 1])
        else:
            # Note that split_key[i + 1] is a bogus empty string.
            parts.extend(map(int, re.findall(r'\d+', sep)))
    return parts


def _unparse_key(parsed):
    bits = []
    for part in parsed:
        if isinstance(part, string_type):
            fmt = ".%s" if bits else "%s"
        else:
            fmt = "[%d]"
        bits.append(fmt % part)
    return ''.join(bits)
