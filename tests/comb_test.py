import pytest

import src.yapypcl.combinators.comb as comb
import src.yapypcl.parsers.prim as prim
from src.yapypcl.parsers.parser import ParseErr, Parser, ParseResult, parse


@pytest.mark.parametrize(
    ("parser1", "parser2", "text", "output"),
    [
        (prim.char("a"), prim.char("b"), "abcd", ParseResult.make_ok((["ab"], "cd"))),
        (prim.char("a"), prim.char("b"), "abab", ParseResult.make_ok((["ab"], "ab"))),
        (
            prim.char("a"),
            prim.char("b"),
            "aacd",
            ParseResult.make_err(ParseErr.expected_char("b", "a")),
        ),
    ],
)
def compose_test[T](parser1: Parser[T], parser2: Parser[T], text: str, output: ParseResult[T]):
    assert parse(comb.compose(parser1, parser2), text) == output


@pytest.mark.parametrize(
    ("parser", "text", "output"),
    [
        (prim.char('a'), "aaabc", ParseResult.make_ok(([['a', 'a', 'a']], "bc"))),
        (prim.char('a'), "bc", ParseResult.make_ok(([], "bc"))),
    ],
)
def many0_test[T](parser: Parser[T], text: str, output: ParseResult[list[T]]):
    assert parse(comb.many0(parser), text) == output


@pytest.mark.parametrize(
    ("parser", "text", "output"),
    [
        (prim.char('a'), "aaabc", ParseResult.make_ok(([['a', 'a', 'a']], "bc"))),
        (prim.char('a'), "bc", ParseResult.make_err(ParseErr.expected_char('a', 'b'))),
    ],
)
def many1_test[T](parser: Parser[T], text: str, output: ParseResult[list[T]]):
    assert parse(comb.many1(parser), text) == output
    

@pytest.mark.parametrize(
    ("first", "otherwise", "text", "output"),
    [
        (prim.char('a'), prim.char('b'), "abc", ParseResult.make_ok((['a'], "bc"))),
        (prim.char('a'), prim.char('b'), "bbc", ParseResult.make_ok((['b'], "bc"))),
        (prim.char('a'), prim.char('b'), "cbc", ParseResult.make_err(ParseErr.expected_one_of(['a', 'b'], 'c'))),
    ],
)
def attempt_test[T](first: Parser[T], otherwise: Parser[T], text: str, output: ParseResult[T]):
    assert parse(comb.attempt(first, otherwise), text) == output


