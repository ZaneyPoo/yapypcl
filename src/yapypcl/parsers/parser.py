"""
yapypcl -- parser.py

Foundational types for parsers

Zane Hargis -- Copyright 2024
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, cast


class ResultKind(Enum):
    Ok = auto()
    Err = auto()


class ParseErrKind(Enum):
    UnexpectedEof = auto()
    ExpectedChar = auto()
    ExpectedOneOf = auto()


@dataclass(slots=True)
class ParseErr:
    kind: ParseErrKind
    data: dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        match self.kind:
            case ParseErrKind.ExpectedChar:
                return f"Expected char: '{self.data['char']}', got: '{self.data['got']}'"

            case ParseErrKind.ExpectedOneOf:
                return f"Expected one of '{self.data['tokens']}', got '{self.data['got']}'"

            case _:
                return self.kind.name

    @staticmethod
    def unexpected_eof() -> ParseErr:
        return ParseErr(ParseErrKind.UnexpectedEof)

    @staticmethod
    def expected_char(char: str, got: str) -> ParseErr:
        return ParseErr(ParseErrKind.ExpectedChar, {"char": char, "got": got})


    @staticmethod
    def expected_one_of(tokens: list[str], got) -> ParseErr:
        return ParseErr(ParseErrKind.ExpectedOneOf, {"tokens": tokens, "got": got})


# FIXME: This typename could easily be misread; it should be renamed.
type Parsed[T] = tuple[list[T], str]


# TODO: Maybe move this into the ParseResult namespace?
class UnwrapException(Exception): ...

# FIXME: Very verbose name. Rename?
class ParseConstructionException(Exception): ...

@dataclass(slots=True)
class ParseResult[T]:
    kind: ResultKind
    data: Parsed[T] | ParseErr

    def __repr__(self) -> str:
        return f"{self.kind.name}({self.data})"

    # @staticmethod
    # def is_err(result: ParseResult[T]) -> TypeGuard[ParseErr]:
    #     return result.kind is ResultKind.Err
    #
    # @staticmethod
    # def is_ok(result: ParseResult[T]) -> TypeGuard[Parsed[T]]:
    #     return result.kind is ResultKind.Ok

    def is_err(self) -> bool:
        return self.kind is ResultKind.Err

    def is_ok(self) -> bool:
        return self.kind is ResultKind.Ok

    def expect(self, message: str = "tried to unwrap an invalid result") -> Parsed[T]:
        if self.is_err():
            raise UnwrapException(message)
        return cast(Parsed[T], self.data)

    @staticmethod
    def make_err(err: ParseErr) -> ParseResult:
        return ParseResult(ResultKind.Err, err)

    @staticmethod
    def make_ok(data: Parsed[T]) -> ParseResult[T]:
        return ParseResult(ResultKind.Ok, data)


# TODO: Add type variable for both input and output types, not just output
type Parser[T] = Callable[[str], ParseResult[T]]

# TODO: Consider using Generators to allow proper method chaining 
#       a la Rust's combinator libraries
def parse[T](parser: Parser[T], text: str) -> ParseResult[T]:
    """
    Parse a string using the given parser.
    """
    return parser(text)
