"""
yapypcl -- parser.py

Foundational types for parsers

Zane Hargis -- Copyright 2024
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Literal


class ResultKind(Enum):
    Ok = auto()
    Err = auto()


class ParseErrKind(Enum):
    UnexpectedEof = auto()
    ExpectedChar = auto()


@dataclass
class ParseErr:
    kind: ParseErrKind
    data: dict[str, str] = field(default_factory=dict)

    def __repr__(self) -> str:
        match self.kind:
            case ParseErrKind.ExpectedChar:
                return f"Expected char: {self.data['char']}, got: '{self.data['got']}'"

            case _:
                return self.kind.name

    @staticmethod
    def unexpected_eof() -> ParseErr:
        return ParseErr(ParseErrKind.UnexpectedEof)

    @staticmethod
    def expected_char(char: str, got: str) -> ParseErr:
        return ParseErr(ParseErrKind.ExpectedChar, {char: char, got: got})


@dataclass
class ParseResult[T]:
    kind: ResultKind
    data: tuple[list[T], str] | ParseErr

    def __repr__(self) -> str:
        if self.kind == ResultKind.Ok:
            return f"Ok({self.data})"
        return f"Err({self.kind.name}: {self.data})"

    @staticmethod
    def make_err(err: ParseErr) -> ParseResult:
        return ParseResult(ResultKind.Err, err)

    @staticmethod
    def make_ok(data: tuple[list[T], str]) -> ParseResult[T]:
        return ParseResult(ResultKind.Ok, data)


type Parser[T] = Callable[[str], ParseResult[T]]


def parse[T](parser: Parser[T], text: str) -> ParseResult[T]:
    """
    Parse a string using the given parser.
    """
    return parser(text)
