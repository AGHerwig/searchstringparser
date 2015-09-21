# -*- coding: utf-8 -*-


from __future__ import (absolute_import, unicode_literals)


"""
====================================
PostgreSQL Search Token Parser Tests
====================================

:Authors:
    Moritz Emanuel Beber
:Date:
    2015-09-18
:Copyright:
    Copyright |c| 2015, Max-Plank-Institute for Molecular Genetics, all rights reserved.
:File:
    test_postgresql.py

.. |c| unicode: U+A9
"""


import pytest

from searchstringparser import PostgreSQLTextSearchParser


@pytest.fixture
def parser():
    return PostgreSQLTextSearchParser()

class TestGeneralSearchStringLexer(object):
    @pytest.mark.parametrize("query,expected", [
        ("stuff", "stuff"),
        ("stuff stuff", "stuff & stuff"),
        ("stuff  \t \r \nstuff", "stuff & stuff"),
        ("stuff stuff", "stuff & stuff"),
        ("stuff*", "stuff:*"),
        ("-stuff", "!stuff"),
        ("- stuff", "!stuff"),
        ("~stuff", "!stuff"),
        ("~ stuff", "!stuff"),
        ("!stuff", "!stuff"),
        ("! stuff", "!stuff"),
        ("not stuff", "!stuff"),
        ("NOT stuff", "!stuff"),
        ("stuff & stuff", "stuff & stuff"),
        ("stuff && stuff", "stuff & stuff"),
        ("stuff and stuff", "stuff & stuff"),
        ("stuff AND stuff", "stuff & stuff"),
        ("stuff | stuff", "stuff | stuff"),
        ("stuff || stuff", "stuff | stuff"),
        ("stuff or stuff", "stuff | stuff"),
        ("stuff OR stuff", "stuff | stuff"),
        ("(stuff OR stuff)", "(stuff | stuff)"),
        ("(good stuff) (more stuff)", "(good & stuff) & (more & stuff)"),
        ("'stuff'", "'stuff'"),
        ("\"stuff\"", "'stuff'"),
        ("\"stuff goes on\"", "'stuff goes on'"),
        ("\"stuff '\"", "'stuff '''"),
        ("\"stuff 'goes\\\" on\"", "'stuff ''goes'' on'"),
        ("(good stuff) || (more 'almost \"decent\"' stuff)",
            "(good & stuff) | (more & 'almost ''decent''' & stuff)"),
    ])
    def test_parse(self, parser, query, expected):
        output = parser.parse(query)
        assert output == expected

    @pytest.mark.parametrize("query,expected", [
        ("stuff", "stuff"),
        ("%stuff;", "stuff")
    ])
    def test_illegal(self, parser, query, expected):
        output = parser.parse(query)
        assert output == expected

