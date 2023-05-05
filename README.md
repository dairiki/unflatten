# unflatten - convert flat dict to nested dict/array

[![Latest Version](https://img.shields.io/pypi/v/unflatten.svg)](https://pypi.python.org/pypi/unflatten/)
[![Python versions](https://img.shields.io/pypi/pyversions/unflatten.svg)]( https://pypi.python.org/pypi/unflatten/)
[![CI test status](https://github.com/dairiki/unflatten/actions/workflows/tests.yml/badge.svg)](https://github.com/dairiki/unflatten/actions/workflows/tests.yml)
[![Trackgit Views](https://us-central1-trackgit-analytics.cloudfunctions.net/token/ping/lhasvnk7wy5gn9qxjmlh)](https://trackgit.com)

## Description

This package provides a function which can unpack a flat dictionary
into a structured `dict` with nested sub-dicts and/or sub-lists.

Development takes place on [github](https://github.com/dairiki/unflatten/).
The package is installable from [PyPI](https://pypi.python.org/pypi/unflatten/).

## Synopsis

Nested dicts:

```pycon
>>> from unflatten import unflatten

>>> unflatten({'foo.bar': 'val'})
{'foo': {'bar': 'val'}}

```

Nested list:

```pycon
>>> unflatten({'foo[0]': 'x', 'foo[1]': 'y'})
{'foo': ['x', 'y']}

```

Nested lists and dicts, intermixed:

```pycon
>>> unflatten({
...     'foo[0][0]': 'a',
...     'foo[0][1]': 'b',
...     'foo[1].x': 'c',
...      })
{'foo': [['a', 'b'], {'x': 'c'}]}

```

## Notes

`Unflatten` takes a single argument which should either be a `dict`
(or an object with a dict-like `.items()` or `.iteritems()`
method) or a sequence of `(key, value)` pairs.
All keys in the dict or sequence must be strings.
(Under python 2, keys must be instances of `basestring`; under
python 3, keys just be instances of `str`.)


`Unflatten` always returns a `dict`.  By way of example:

```pycon
>>> unflatten([('[0]', 'x')])
{'': ['x']}

```

For list-valued nodes, all indexes must be present in the input
(flattened) mapping, otherwise a `ValueError` will be thrown:

```pycon
>>> unflatten({'a[0]': 'x', 'a[2]': 'y'})
Traceback (most recent call last):
...
ValueError: missing key 'a[1]'

```

## See Also

The [morph] and [flattery] packages purport to implement similar functions.

[morph]: https://github.com/metagriffin/morph
[flattery]: https://github.com/acg/python-flattery

## Authors

[Jeff Dairiki](mailto:dairiki@dairiki.org)
