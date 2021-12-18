==================================================
unflatten - convert flat dict to nested dict/array
==================================================

|version| |pyversions| |build status|

***********
Description
***********

This package provides a function which can unpack a flat dictionary
into a structured ``dict`` with nested sub-dicts and/or sub-lists.

Development takes place on github_.
The package is installable from PyPI_

.. _github: https://github.com/dairiki/unflatten/
.. _pypi: https://pypi.python.org/pypi/unflatten/

********
Synopsis
********

Nested dicts::

  >>> from unflatten import unflatten

  >>> unflatten({'foo.bar': 'val'})
  {'foo': {'bar': 'val'}}

Nested list::

  >>> unflatten({'foo[0]': 'x', 'foo[1]': 'y'})
  {'foo': ['x', 'y']}

Nested lists and dicts, intermixed::

  >>> unflatten({
  ...     'foo[0][0]': 'a',
  ...     'foo[0][1]': 'b',
  ...     'foo[1].x': 'c',
  ...      })
  {'foo': [['a', 'b'], {'x': 'c'}]}


*****
Notes
*****

``Unflatten`` takes a single argument which should either be a ``dict``
(or an object with a dict-like ``.items()`` or ``.iteritems()``
method) or a sequence of ``(key, value)`` pairs.
All keys in the dict or sequence must be strings.
(Under python 2, keys must be instances of ``basestring``; under
python 3, keys just be instances of ``str``.)


``Unflatten`` always returns a ``dict``.  By way of example::

  >>> unflatten([('[0]', 'x')])
  {'': ['x']}

For list-valued nodes, all indexes must be present in the input
(flattened) mapping, otherwise a ``ValueError`` will be thrown::

  >>> unflatten({'a[0]': 'x', 'a[2]': 'y'})
  Traceback (most recent call last):
  ...
  ValueError: missing key 'a[1]'

********
See Also
********

The `morph`_ and `flattery`_ packages purport to implement similar functions.

.. _morph: https://github.com/metagriffin/morph
.. _flattery: https://github.com/acg/python-flattery

*******
Authors
*******

`Jeff Dairiki`_

.. _Jeff Dairiki: mailto:dairiki@dairiki.org

.. |version| image::
    https://img.shields.io/pypi/v/unflatten.svg
    :target: https://pypi.python.org/pypi/unflatten/
    :alt: Latest Version

.. |pyversions| image::
    https://img.shields.io/pypi/pyversions/unflatten.svg
    :target: https://pypi.python.org/pypi/unflatten/
    :alt: Python versions

.. |build status| image::
    https://github.com/dairiki/unflatten/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/dairiki/unflatten/actions/workflows/tests.yml
 
