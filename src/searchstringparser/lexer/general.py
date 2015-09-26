# -*- coding: utf-8 -*-


from __future__ import (absolute_import, print_function)


"""
=================================
General Search String Token Lexer
=================================

:Authors:
    Moritz Emanuel Beber
:Date:
    2015-09-16
:Copyright:
    Copyright |c| 2015, Max Plank Institute for Molecular Genetics, all rights reserved.
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
       "WORD",
       "WILDCARD",
       "NOT",
       "AND",
       "OR",
       "LPAREN",
       "RPAREN",
       "SYMBOL",
       "LITERAL_QUOTE",
       "SPACE",
       "QUOTE"
    )

    # A string containing ignored characters (spaces and tabs)
    t_ignore = " \t\r\n\f\v"  # whitespace (interpreted literally not as regex)
    # Regular expression rules for simple tokens
    t_WORD = r"\w+"
    t_WILDCARD = r"\*"
    t_NOT = r"-|~|!|not|NOT"
    t_AND = r"&{1,2}|and|AND"
    t_OR = r"\|{1,2}|or|OR"
    # rules for 'quoting' state
    t_quoting_ignore = ""
    t_quoting_SYMBOL = r"([^'\"\s\\]|\\(?!'|\"))+"  # anything but other tokens

    def __init__(self, illegal="ignore", **kw_args):
        super(GeneralSearchStringLexer, self).__init__()
# pick between different error handling methods
        self.lexer = lex.lex(module=self, **kw_args)
        self.parens_level = 0
        self._quote_start = None
        self._invalid = None
        self._invalid_pos = None

    def __getattr__(self, attr):
        return getattr(self.lexer, attr)

    def __iter__(self):
        return (tok for tok in iter(self.lexer.token, None))

    def input(self, data):
        self.parens_level = 0
        self._quote_start = None
        self._invalid = list()
        self._invalid_pos = list()
        self.lexer.input(data)

    def get_illegal(self):
        if not self._invalid:
            return None
        return (self._invalid, self._invalid_pos)

    # inspect output
    def print_tokens(self, data):
        self.input(data)
        for tok in self:
            print(tok)
        if self._invalid:
            print("Invalid character(s): " + ", ".join(self._invalid))
            print("at position(s): " + ", ".join([str(x) for x in self._invalid_pos]))

    # Error handling rule
    def t_ANY_error(self, t):
        self._invalid.append(t.value[0])
        self._invalid_pos.append(t.lexpos)
        t.lexer.skip(1)

    def t_LPAREN(self, t):
        r"\("
        self.parens_level += 1
        return t

    def t_RPAREN(self, t):
        r"\)"
        self.parens_level -= 1
        return t

    # quoting state
    def t_quoting_LITERAL_QUOTE(self, t):
        r"\\'|\\\""
        return t

    def t_QUOTE(self, t):
        r"'|\""
        self._quote_start = t.lexer.lexpos
        t.lexer.push_state("quoting")
        return t

    def t_quoting_QUOTE(self, t):
        r"'|\""
        # handle different quote inside quote
        if t.value != t.lexer.lexdata[self._quote_start - 1]:
            t.type = "LITERAL_QUOTE"
            return t
        t.lexer.pop_state()
        return t

    def t_quoting_SPACE(self, t):
        r"\s+"
        return t

