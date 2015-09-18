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
#        ("stuff  \t \r \nstuff", ("WORD", "WORD")),
#        ("stuff stuff", ("WORD", "WORD")),
#        ("stuff*", ("WORD", "WILDCARD")),
#        ("-stuff", ("NOT", "WORD")),
#        ("- stuff", ("NOT", "WORD")),
#        ("~stuff", ("NOT", "WORD")),
#        ("~ stuff", ("NOT", "WORD")),
#        ("!stuff", ("NOT", "WORD")),
#        ("! stuff", ("NOT", "WORD")),
#        ("not stuff", ("NOT", "WORD")),
#        ("NOT stuff", ("NOT", "WORD")),
#        ("stuff & stuff", ("WORD", "AND", "WORD")),
#        ("stuff && stuff", ("WORD", "AND", "WORD")),
#        ("stuff and stuff", ("WORD", "AND", "WORD")),
#        ("stuff AND stuff", ("WORD", "AND", "WORD")),
#        ("stuff | stuff", ("WORD", "OR", "WORD")),
#        ("stuff || stuff", ("WORD", "OR", "WORD")),
#        ("stuff or stuff", ("WORD", "OR", "WORD")),
#        ("stuff OR stuff", ("WORD", "OR", "WORD")),
    ])
    def test_parse(self, parser, query, expected):
        output = parser.parse(query)
        assert output == expected

#    @pytest.mark.parametrize("query,illegal", [
#        ("stuff", None),
#        ("%stuff;", (["%", ";"], [0, 6]))
#    ])
#    def test_illegal(self, lexer, query, illegal):
#        lexer.input(query)
#        # consume input s.t. tokens are generated
#        for _ in lexer:
#            pass
#        assert lexer.get_illegal() == illegal

