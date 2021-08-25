from typing import List

import expr
import parser
import scanner
import statem


def source_to_statements(source: str) -> List[statem.Statem]:
    """ """
    searcher = scanner.init_scanner(source=source)
    tokens = scanner.scan(searcher)
    processor = parser.init_parser(tokens=tokens)
    return parser.parse(processor)


def test_parse() -> None:
    """ """
    statements = source_to_statements(source="1 * (2 + 3);")
    assert len(statements) == 1

    statement = statements[0]
    assert isinstance(statement, statem.Expression)

    expression = statement.expression
    assert isinstance(expression, expr.Binary)
    assert isinstance(expression.left, expr.Literal)
    assert isinstance(expression.right, expr.Grouping)
    assert expression.operator.token_type == scanner.TokenType.STAR
    assert isinstance(expression.right.expression, expr.Binary)
    assert isinstance(expression.right.expression.left, expr.Literal)
    assert isinstance(expression.right.expression.right, expr.Literal)
    assert expression.right.expression.operator.token_type == scanner.TokenType.PLUS
