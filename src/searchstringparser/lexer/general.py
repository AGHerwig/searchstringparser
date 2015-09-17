# -*- coding: utf-8 -*-


from __future__ import (absolute_import, unicode_literals, print_function)


"""
=================================
General Search String Token Lexer
=================================

:Authors:
    Moritz Emanuel Beber
:Date:
    2015-09-16
:Copyright:
    Copyright |c| 2015, Max-Plank-Institute for Molecular Genetics, all rights reserved.
:File:
    general.py

.. |c| unicode: U+A9
"""


__all__ = ["GeneralSearchStringLexer"]


import ply.lex as lex


class GeneralSearchStringLexer(object):
    states = (
        ("quoting", "exclusive"),
    )
    # List of token names.   This is always required
    tokens = (
       "SYMBOL",
       "SPACE",
       "WORD",
       "AND",
       "OR",
       "NOT",
       "WILDCARD",
       "LITERAL_QUOTE",
       "QUOTE",
       "LPAREN",
       "RPAREN"
    )

    # A string containing ignored characters (spaces and tabs)
    t_ANY_ignore  = "\f\v" # unusual whitespace
    t_ANY_SPACE = r"[ \t\r\n]+"
    t_WORD = r"\w+"
    # Regular expression rules for simple tokens
    t_AND = r"&{1,2}|and|AND"
    t_OR = r"\|{1,2}|or|OR"
    t_NOT = r"-|~|!|not|NOT"
    t_WILDCARD = r"\*"
    # rules for 'quoting' state
    t_quoting_SYMBOL = r"[^'\" \t\r\n]+" # anything but whitespace and quotes

    def __init__(self, **kw_args):
        super(GeneralSearchStringLexer, self).__init__()
        self.lexer = lex.lex(module=self, **kw_args)
        self.parens_level = 0
        self._invalid = None
        self._invalid_pos = None
        self._quote_start = None

    def t_quoting_LITERAL_QUOTE(self, t):
        r"\\'|\\\""
        return t

    def t_QUOTE(self, t):
        r"'|\""
        self._quote_start = t.lexer.lexpos
        t.lexer.push_state("quoting")
        return t

    def t_quoting_QUOTE(self, t):
        r'\'|"'
        # handle different quote inside quote
        if t.value != t.lexer.lexdata[self._quote_start - 1]:
            t.type = "LITERAL_QUOTE"
            return t
        t.lexer.pop_state()
        return t

    def t_LPAREN(self, t):
        r"\("
        self.parens_level += 1
        return t

    def t_RPAREN(self, t):
        r"\)"
        self.parens_level -= 1
        return t

    # Error handling rule
    def t_ANY_error(self, t):
        self._invalid.append(t.value[0])
        self._invalid_pos.append(t.lexpos)
        t.lexer.skip(1)

    # test output
    def test(self, data):
        self._invalid = list()
        self._invalid_pos = list()
        self.lexer.input(data)
        for tok in iter(self.lexer.token, None):
            print(tok)
        if self._invalid:
            print("Invalid character(s): " + ", ".join(self._invalid))
            print("at position(s): " + ", ".join([str(x) for x in self._invalid_pos]))

