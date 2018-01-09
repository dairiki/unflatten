==================================================
unflatten - convert flat dict to nested dict/array
==================================================

|version| |pyversions| |build status|

***********
Description
***********

This package provides a function which can unpack a flat dictionary
into a ``dict`` with nested ``dict``\s and ``list``\s.

For example::

    >>> unflatten({
    ...    'a[0].b': 'a0b',
    ...    'a[1].c': 'a1c',
    ...    'd.e': 'de',
    ...    })
    {'a': [{'b': 'a0b'}, {'c': 'a1c'}], 'd': {'e': 'de'}}

Development takes place on github_.
The package is installable from PyPI_

.. _github: https://github.com/dairiki/unflatten/
.. _pypi: https://pypi.python.org/pypi/unflatten/

********
Synopsis
********


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
    https://travis-ci.org/dairiki/unflatten.svg?branch=master
    :target: https://travis-ci.org/dairiki/unflatten
