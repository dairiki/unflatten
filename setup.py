# -*- coding: utf-8 -*-
from setuptools import setup
import sys

VERSION = '0.1b1.post1.dev0'

with open('README.rst') as readme_file:
    README = readme_file.read()
with open('CHANGES.rst') as changes_file:
    CHANGES = changes_file.read()

requires = [
    ]

tests_require = [
    'pytest',
    ]

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

setup(
    name='unflatten',
    version=VERSION,
    description="Unflatten dict to dict with nested dict/arrays",
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    author='Jeff Dairiki',
    author_email='dairiki@dairiki.org',
    url='https://github.com/dairiki/unflatten',
    keywords='unflatten nested-dict',

    py_modules=['unflatten'],
    package_dir={'': 'src'},
    install_requires=requires,
    setup_requires=pytest_runner,
    tests_require=tests_require,
    extras_require={
        "test": tests_require,
        },

    include_package_data=True,
    zip_safe=True,
    )
