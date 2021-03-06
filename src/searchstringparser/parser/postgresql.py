# -*- coding: utf-8 -*-


"""
==============================
PostgreSQL Search Token Parser
==============================

:Authors:
    Moritz Emanuel Beber
:Date:
    2015-09-16
:Copyright:
    Copyright |c| 2015, Max Plank Institute for Molecular Genetics,
    all rights reserved.
:File:
    postgresql.py

.. |c| unicode: U+A9
"""


from __future__ import absolute_import

import ply.yacc as yacc

from ..lexer import GeneralSearchStringLexer


__all__ = ["PostgreSQLTextSearchParser"]


class PostgreSQLTextSearchParser(object):
    """
    This parser implements the following rules using the tokens generated by an
    appropriate lexer. The goal is to generate a string for PostgreSQL full text
    search that conforms with the syntax understood by the function `tsquery or
    to_tsquery
    <http://www.postgresql.org/docs/9.4/static/datatype-textsearch.html#DATATYPE-TSQUERY>`_.

    The following rules are implemented which generate the correct query string.

    ::

        expression : expression expression
                   | expression AND expression
                   | expression OR expression
                   | NOT expression
                   | LPAREN expression RPAREN
                   | QUOTE term QUOTE
                   | WORD WILDCARD
                   | WORD

        term : term SPACE term
               | term term
               | LITERAL_QUOTE
               | SYMBOL
               
    """  # noqa

    precedence = (
        ("left", "OR"),
        ("left", "AND", "SPACE"),
        ("right", "NOT"),
        ("left", "WILDCARD")
    )

    def __init__(self, lexer=None, **kw_args):
        """Parser instantiation.

        Parameters
        ----------
        lexer : ply.lex (optional)
            Any ply.lex lexer instance and generates the tokens listed in the
            rules. The default uses a GeneralSearchStringLexer instance.
        kw_args :
            Keyword arguments are passed to the ply.yacc.yacc call.

        """
        super(PostgreSQLTextSearchParser, self).__init__()
        self.lexer = GeneralSearchStringLexer() if lexer is None else lexer
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, **kw_args)

    def parse(self, query, **kw_args):
        """Parse any string input according to the rules.

        Parameters
        ----------
        query : str
            A string expected to conform with the search query syntax.
        kw_args :
            Keyword arguments are passed on to the ply.yacc.yacc.parse call.

        Returns
        -------
        str
            A string that can directly be passed to the PostgreSQL functions
            `tsquery or to_tsquery <http://www.postgresql.org/docs/9.4/static/datatype-textsearch.html#DATATYPE-TSQUERY>`_.
            
        """  # noqa
        self.lexer._invalid = list()
        self.lexer._invalid_pos = list()
        return self.parser.parse(query, lexer=self.lexer, **kw_args)

    def get_illegal(self):
        """Inspect encountered illegal characters.

        Returns
        -------
        None
            If no illegal characters occurred.
        Tuple
            A pair of lists that contain the illegal characters and
            the positions where they occurred.
        """
        self.lexer.get_illegal()

    def p_error(self, p):
        if p is None:
            if self.lexer.parens_level > 0:
                raise SyntaxError(
                    "{0:d} mismatched parentheses! Last opening"
                    " parenthesis at position {1:d}.".format(
                            self.lexer.parens_level,
                            self.lexer.last_lparens
                    ))
            elif self.lexer.last_quote is not None:
                raise SyntaxError("Unclosed quote at position {0:d}.".format(
                    self.lexer.last_quote
                ))
#            else:  # there should be no other EOF syntax errors
#                raise SyntaxError("Syntax error at EOF!")
        if self.lexer.parens_level < 0:
            raise SyntaxError(
                "{0:d} mismatched parentheses! Last closing"
                " parenthesis at position {1:d}.".format(
                        abs(self.lexer.parens_level),
                        self.lexer.last_rparens
                ))
        else:
            raise SyntaxError(str(p))

    def p_expression_space(self, p):
        """expression : expression expression %prec AND"""
        p[0] = "{0} & {1}".format(p[1], p[2])

    def p_expression_and(self, p):
        """expression : expression AND expression"""
        p[0] = "{0} & {1}".format(p[1], p[3])

    def p_expression_or(self, p):
        """expression : expression OR expression"""
        p[0] = "{0} | {1}".format(p[1], p[3])

    def p_expression_unot(self, p):
        """expression : NOT expression"""
        p[0] = "!{0}".format(p[2])

    def p_expression_parens(self, p):
        """expression : LPAREN expression RPAREN"""
        p[0] = "({0})".format(p[2])

    def p_expression_quoted(self, p):
        """expression : QUOTE term QUOTE"""
        p[0] = "'{0}'".format(p[2])

    def p_expression_word_wildcard(self, p):
        """expression : WORD WILDCARD"""
        p[0] = "{0}:*".format(p[1])

    def p_expression_word(self, p):
        """expression : WORD"""
        p[0] = p[1]

    def p_term_term_space_term(self, p):
        """term : term SPACE term"""
        p[0] = "{0} {1}".format(p[1], p[3])

    def p_term_term_term(self, p):
        """term : term term %prec WILDCARD"""
        p[0] = "{0}{1}".format(p[1], p[2])

    def p_term_literal_quote(self, p):
        """term : LITERAL_QUOTE"""
        p[0] = "''"

    def p_term_symbol(self, p):
        """term : SYMBOL"""
        p[0] = p[1]
