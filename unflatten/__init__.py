# -*- coding: utf-8 -*-
""" Unflatten nested dict/array data

"""
from __future__ import absolute_import

from itertools import groupby
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

    parsed_items = sorted(((_parse_key(key), val) for key, val in items),
                          key=itemgetter(0))
    if len(parsed_items) == 0:
        return {}
    return _unflatten_items(parsed_items, depth=0)


TERMINAL = 0
DICT = 1
LIST = 2
TYPE_NAME = {
    TERMINAL: 'terminal',
    DICT: 'dict',
    LIST: 'list',
    }


def _unflatten_items(parsed_items, depth):
    def node_type(arg):
        parsed_key, val = arg
        if len(parsed_key) == depth:
            return TERMINAL      # terminal
        return parsed_key[depth][0]

    def key(arg):
        parsed_key, val = arg
        return parsed_key[depth][1]

    by_type = groupby(parsed_items, key=node_type)

    type_, group = next(by_type)
    if type_ == TERMINAL:
        for parsed_key, value in group:
            pass                # take last value in group
    elif type_ == LIST:
        value = []
        for ind, items in groupby(group, key=key):
            if len(value) != ind:
                assert len(value) < ind
                parsed_key, _ = next(items)
                prefix = parsed_key[:depth]
                missing_ind = (LIST, len(value))
                missing_key = _unparse_key(prefix + (missing_ind,))
                raise ValueError("missing key %s" % missing_key)
            value.append(_unflatten_items(items, depth=depth + 1))
    else:
        assert type_ == DICT
        value = dict(
            (key_, _unflatten_items(items, depth=depth + 1))
            for key_, items in groupby(group, key=key))

    types = [type_]
    for type_, group in by_type:
        types.append(type_)
        parsed_key, _ = next(group)
    if len(types) > 1:
        types = ' and '.join(TYPE_NAME[_] for _ in types)
        key = _unparse_key(parsed_key[:depth + 1])
        raise ValueError("mixture of %s nodes for %s" % (types, key))

    return value


_INDEX_re = re.compile(r'\[(?P<ind>\d+)\]\Z')


def _parse_key(key):
    if not isinstance(key, string_types):
        raise TypeError("keys must be strings")
    parts = []
    for part in reversed(key.split('.')):
        m = _INDEX_re.search(part)
        while m:
            parts.append((LIST, int(m.group('ind'))))
            part = part[:m.start()]
            m = _INDEX_re.search(part)
        parts.append((DICT, part))
    return tuple(reversed(parts))


def _unparse_key(parsed):
    bits = []
    for type_, part in parsed:
        if type_ == LIST:
            fmt = "[%d]"
        else:
            fmt = ".%s" if bits else "%s"
        bits.append(fmt % part)
    return ''.join(bits)
