Search String Parser
====================

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
    * - package
      - |version| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/searchstringparser/badge/?version=latest
    :target: http://searchstringparser.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/AGHerwig/searchstringparser.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/AGHerwig/searchstringparser

.. |version| image:: https://img.shields.io/pypi/v/searchstringparser.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/searchstringparser

.. |wheel| image:: https://img.shields.io/pypi/wheel/searchstringparser.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/searchstringparser

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/searchstringparser.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/searchstringparser

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/searchstringparser.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/searchstringparser

Parse a more general search syntax to conform with a particular SQL dialect.

Currently, this is implemented using ply_ with a general lexer and a parser for
generating PostgreSQL-specific search queries.

* Free software: BSD license

.. _ply: http://www.dabeaz.com/ply/ply.html

Installation
============

::

    pip install searchstringparser

Documentation
=============

https://searchstringparser.readthedocs.org/

Development
===========

To run the all tests run::

    tox
