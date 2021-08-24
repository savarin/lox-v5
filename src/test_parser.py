from typing import Optional

import expr
import parser
import scanner


def source_to_expression(source: str) -> Optional[expr.Expr]:
    """ """
    searcher = scanner.init_scanner(source=source)
    tokens = scanner.scan(searcher)
    processor = parser.init_parser(tokens=tokens)

    return parser.parse(processor)


def test_parse() -> None:
    """ """
    expression = source_to_expression(source="1 * (2 + 3)")

    assert isinstance(expression, expr.Binary)
    assert isinstance(expression.left, expr.Literal)
    assert isinstance(expression.right, expr.Grouping)
    assert expression.operator.token_type == scanner.TokenType.STAR

    assert isinstance(expression.right.expression, expr.Binary)
    assert isinstance(expression.right.expression.left, expr.Literal)
    assert isinstance(expression.right.expression.right, expr.Literal)
    assert expression.right.expression.operator.token_type == scanner.TokenType.PLUS
