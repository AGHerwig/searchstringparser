# -*- coding: utf-8 -*-


from __future__ import (absolute_import,)


"""
=======================================
General Search String Token Lexer Tests
=======================================

:Authors:
    Moritz Emanuel Beber
:Date:
    2015-09-18
:Copyright:
    Copyright |c| 2015, Max Plank Institute for Molecular Genetics, all rights reserved.
:File:
    test_general.py

.. |c| unicode: U+A9
"""


import io

import pytest

from searchstringparser import GeneralSearchStringLexer

@pytest.fixture
def lexer():
    return GeneralSearchStringLexer()

@pytest.fixture
def general_output():
    return io.open("tests/lexer/general.out").readlines()

class TestGeneralSearchStringLexer(object):
    @pytest.mark.parametrize("query,expected", [
        ("stuff", ("WORD",)),
        ("stuff stuff", ("WORD", "WORD")),
        ("stuff  \t \r \nstuff", ("WORD", "WORD")),
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
        ("(stuff OR stuff)", ("LPAREN", "WORD", "OR", "WORD", "RPAREN")),
        ("(good stuff) (more stuff)", ("LPAREN", "WORD", "WORD", "RPAREN",
            "LPAREN", "WORD", "WORD", "RPAREN")),
        ("'stuff'", ("QUOTE", "SYMBOL", "QUOTE")),
        ("\"stuff\"", ("QUOTE", "SYMBOL", "QUOTE")),
        ("\"stuff goes on\"", ("QUOTE", "SYMBOL", "SPACE", "SYMBOL", "SPACE",
            "SYMBOL", "QUOTE")),
        ("\"stuff '\"", ("QUOTE", "SYMBOL", "SPACE", "LITERAL_QUOTE", "QUOTE")),
        ("\"stuff 'goes\\\" on\"", ("QUOTE", "SYMBOL", "SPACE", "LITERAL_QUOTE",
            "SYMBOL", "LITERAL_QUOTE", "SPACE", "SYMBOL", "QUOTE")),
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

    @pytest.mark.parametrize("query,lines", [
        ("stuff", (0,)),
        ("stuff stuff", (0, 6)),
        ("stuff  \t \r \nstuff", (0, 12)),
        ("stuff*", (0, 15)),
        ("-stuff", (16, 1)),
        ("- stuff", (16, 2)),
        ("~stuff", (17, 1)),
        ("~ stuff", (17, 2)),
        ("!stuff", (18, 1)),
        ("! stuff", (18, 2)),
        ("not stuff", (19, 4)),
        ("NOT stuff", (20, 4)),
        ("stuff & stuff", (0, 21, 8)),
        ("stuff && stuff", (0, 22, 9)),
        ("stuff and stuff", (0, 23, 10)),
        ("stuff AND stuff", (0, 24, 10)),
        ("stuff | stuff", (0, 25, 8)),
        ("stuff || stuff", (0, 26, 9)),
        ("stuff or stuff", (0, 27, 9)),
        ("stuff OR stuff", (0, 28, 9)),
        ("(stuff OR stuff)", (30, 1, 29, 10, 32)),
        ("(good stuff) (more stuff)", (30, 35, 6, 33, 31, 36, 37, 34)),
        ("'stuff'", (38, 42, 39)),
        ("\"stuff\"", (40, 42, 41)),
        ("\"stuff goes on\"", (40, 42, 46, 43, 47, 44, 45)),
        ("\"stuff '\"", (40, 42, 46, 48, 49)),
        ("stuff", (0,)),
        ("%stuff;", (1, 50, 51))
    ])
    def test_print(self, lexer, capsys, general_output, query, lines):
        lexer.print_tokens(query)
        (out, err) = capsys.readouterr()
        expected = "".join(general_output[i] for i in lines)
        print(query)
        assert out == expected
        assert err == ""

