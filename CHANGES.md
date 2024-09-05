
## History

### Release 0.2.0 (2024-09-04)

No substantive code changes from 0.1.1.

#### Features

- Added type annotations.

#### Testing

- Test under python 3.10, 3.11, and 3.12.

- Fix tox config to cope with the fact that recent tox/virtualenv does
  not support EOLed versions of python.

### Release 0.1.1 (2021-08-16)

#### Nits

- Fix backslashes in docstrings

#### Packaging

- PEP517-ize the packaging
- Use `setuptools-scm` to maintain version numbers

#### Testing

- Test under Python 3.7, 3.8, 3.9 and PyPy 3.7. Drop testing for Python 3.4 & 3.5.
- Pin pip version for pypy2 (see [pip #8653][])
- Clean up and modernize the tox `lint` and `coverage` environments

[pip #8653]: https://github.com/pypa/pip/issues/8653


### Release 0.1 (2018-01-17)

No code changes.

This package is now deemed "production ready" (though your mileage may vary.)

### Release 0.1b1 (2018-01-09)

Initial release.
