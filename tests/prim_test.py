import src.yapypcl.parsers.prim as prim
from src.yapypcl.parsers.parser import parse, ParseResult, ParseErr
import pytest

@pytest.mark.parametrize(
    ('ch', "text", "output"),
    [
        ('a', "abc", ParseResult.make_ok((['a'], "bc"))),
        ('a', "bbc", ParseResult.make_err(ParseErr.expected_char('a', 'b'))),
    ],
)
def char_test[T](ch: str, text: str, output: ParseResult[T]):
    assert parse(prim.char(ch), text) == output


@pytest.mark.parametrize(
    ("sequence", "text", "output"),
    [
        ("yield", "yield 123 + 456", ParseResult.make_ok((["yield"], "123 + 456"))),
        ("yield", "yieldyieldyield", ParseResult.make_ok((["yield"], "yieldyield"))),
        ("yield", "yeld 123 + 456", ParseResult.make_err(ParseErr.expected_char('i', 'e'))),
    ],
)
def token_test[T](sequence: str, text: str, output: ParseResult[T]):
    assert parse(prim.token(sequence), text) == output
