"""
yapypcl -- combinators.comb.py

Primitive combinators

Zane Hargis -- Copyright 2024
"""

from typing import cast
from src.yapypcl.parsers.parser import Parsed, Parser, ParseResult


def compose[T](parser1: Parser[T], parser2: Parser[T]) -> Parser[T]:
    def parser(text: str) -> ParseResult[T]:
        result1 = parser1(text)
        if result1.is_err():
            return result1

        (nommed1, remaining) = cast(Parsed[T], result1.data)
        result2 = parser2(remaining)
        if result2.is_err():
            return result2
        (nommed2, remaining) = cast(Parsed[T], result2.data)

        return ParseResult.make_ok(([*nommed1, *nommed2], remaining))

    return parser
