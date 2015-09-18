# -*- coding: utf-8 -*-


from __future__ import (absolute_import, unicode_literals)


"""
=======================================
General Search String Token Lexer Tests
=======================================

:Authors:
    Moritz Emanuel Beber
:Date:
    2015-09-18
:Copyright:
    Copyright |c| 2015, Max-Plank-Institute for Molecular Genetics, all rights reserved.
:File:
    test_general.py

.. |c| unicode: U+A9
"""


import pytest

from searchstringparser import GeneralSearchStringLexer

@pytest.fixture
def lexer():
    return GeneralSearchStringLexer()

class TestGeneralSearchStringLexer(object):
    @pytest.mark.parametrize("query,expected", [
        ("stuff", ("WORD",)),
        ("stuff stuff", ("WORD", "WORD")),
        ("stuff  \t \r \nstuff", ("WORD", "WORD")),
        ("stuff stuff", ("WORD", "WORD")),
        ("stuff*", ("WORD", "WILDCARD")),
        ("-stuff", ("NOT", "WORD")),
        ("- stuff", ("NOT", "WORD")),
        ("~stuff", ("NOT", "WORD")),
        ("~ stuff", ("NOT", "WORD")),
        ("!stuff", ("NOT", "WORD")),
        ("! stuff", ("NOT", "WORD")),
        ("not stuff", ("NOT", "WORD")),
        ("NOT stuff", ("NOT", "WORD")),
        ("stuff & stuff", ("WORD", "AND", "WORD")),
        ("stuff && stuff", ("WORD", "AND", "WORD")),
        ("stuff and stuff", ("WORD", "AND", "WORD")),
        ("stuff AND stuff", ("WORD", "AND", "WORD")),
        ("stuff | stuff", ("WORD", "OR", "WORD")),
        ("stuff || stuff", ("WORD", "OR", "WORD")),
        ("stuff or stuff", ("WORD", "OR", "WORD")),
        ("stuff OR stuff", ("WORD", "OR", "WORD")),
    ])
    def test_token(self, lexer, query, expected):
        lexer.input(query)
        tokens = tuple(tok.type for tok in lexer)
        assert tokens == expected

    @pytest.mark.parametrize("query,illegal", [
        ("stuff", None),
        ("%stuff;", (["%", ";"], [0, 6]))
    ])
    def test_illegal(self, lexer, query, illegal):
        lexer.input(query)
        # consume input s.t. tokens are generated
        for _ in lexer:
            pass
        assert lexer.get_illegal() == illegal

