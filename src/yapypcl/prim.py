"""
yapypcl -- prim.py 

Primitive parsers

Zane Hargis -- Copyright 2024
"""

from .parser import parse, ParseErr, Parser, ParseResult


def spec_char[T](char: str) -> Parser[T]:
    """ 
    Return a parser which matches for a specific character

    >>> parse(spec_char('a'), "abcd")
    
    """
    def parser(text: str) -> ParseResult[T]:
        if text[0] == char[0]:
            return ParseResult.make_ok(([char], text[1:]))
        else:
            return ParseResult.make_err(ParseErr.expected_char(char, text[0]))

    return parser
