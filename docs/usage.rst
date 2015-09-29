=====
Usage
=====

To use Search String Parser in a project::

	import searchstringparser

or directly import one of the :doc:`lexers <reference/searchstringparser.lexer>` or :doc:`parsers <reference/searchstringparser.parser>`, e.g.,

::

    >>> from searchstringparser import GeneralSearchStringLexer
    >>> from searchstringparser import PostgreSQLTextSearchParser

You can then use an instance of the lexer for your own parser or parse a search
query string.

::

    >>> parser = PostgreSQLTextSearchParser()
    >>> parser.parse("find my term")
    'find & my & term'

