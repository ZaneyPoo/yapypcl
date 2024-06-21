"""
yapypcl -- prim.py 

Primitive parsers

All of these parsers default to matching exactly once.
In order to match an arbitrary number of occurrences,
compose them with a combinator.

Zane Hargis -- Copyright 2024
"""

from .parser import ParseErr, Parser, ParseResult


def char[T](ch: str) -> Parser[T]:
    """
    Return a parser which matches a specific character.

    Examples: 
    >>> parse(char('a'), "abc")
    Ok((['a'], 'bc'))
    """
    ch = ch[0]
    def parser(text: str) -> ParseResult[T]:
        if text[0] == ch:
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
