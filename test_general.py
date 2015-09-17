
import sys
sys.path.insert(0, "src")

from searchstringparser import (GeneralSearchStringLexer,
        PostgreSQLTextSearchParser)

def test_general():
    lexer = GeneralSearchStringLexer()
    query = "stuff 'in quotes \\' is   good \"stuff'"
    lexer.test(query)

def test_postgre():
    parser = PostgreSQLTextSearchParser()
    query = "stuff 'in quotes \\' is   good \"stuff'"
    print(parser.parse(query))

if __name__ == "__main__":
    test_general()
    test_postgre()

