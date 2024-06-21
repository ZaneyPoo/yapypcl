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
