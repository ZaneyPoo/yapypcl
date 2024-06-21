"""
yapypcl -- prim.py 

Primitive parsers

Zane Hargis -- Copyright 2024
"""

from .parser import ParseErr, Parser, ParseResult


def char[T](ch: str) -> Parser[T]:
    def parser(text: str) -> ParseResult[T]:
        if text[0] == ch[0]:
            return ParseResult.make_ok(([ch], text[1:]))
        else:
            return ParseResult.make_err(ParseErr.expected_char(ch, text[0]))

    return parser


def token[T](sequence: str) -> Parser[T]:
    """
    Return a parser which matches for a specific sequence of characters exactly once.

    """
    
    def parser(text: str) -> ParseResult[T]:
        # TODO: Implement me!!!
        ...

    return parser
