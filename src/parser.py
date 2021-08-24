from typing import List, Optional, Tuple
import dataclasses

import expr
import scanner


class ParseError(Exception):
    """ """

    pass


@dataclasses.dataclass
class Parser:
    """ """

    tokens: List[scanner.Token]
    current: int


def init_parser(tokens: List[scanner.Token]) -> Parser:
    """ """
    return Parser(tokens=tokens, current=0)


def parse(processor: Parser) -> Optional[expr.Expr]:
    """ """
    try:
        _, individual_expression = term(processor)
        return individual_expression

    except ParseError:
        return None


def term(processor: Parser) -> Tuple[Parser, expr.Expr]:
    """ """
    processor, factor_expression = factor(processor)

    while True:
        processor, is_match = match(processor, [scanner.TokenType.PLUS])

        if not is_match:
            break

        operator = previous(processor)
        processor, right = factor(processor)
        factor_expression = expr.Binary(factor_expression, operator, right)

    return processor, factor_expression


def factor(processor: Parser) -> Tuple[Parser, expr.Expr]:
    """ """
    processor, primary_expression = primary(processor)

    while True:
        processor, is_match = match(processor, [scanner.TokenType.STAR])

        if not is_match:
            break

        operator = previous(processor)
        processor, right = primary(processor)
        primary_expression = expr.Binary(primary_expression, operator, right)

    return processor, primary_expression


def primary(processor: Parser) -> Tuple[Parser, expr.Expr]:
    """ """
    processor, is_match = match(processor, [scanner.TokenType.NUMBER])

    if is_match:
        value = previous(processor).literal

        assert value is not None
        return processor, expr.Literal(value)

    processor, is_match = match(processor, [scanner.TokenType.LEFT_PAREN])

    if is_match:
        processor, individual_expression = term(processor)
        processor, _ = consume(
            processor, scanner.TokenType.RIGHT_PAREN, "Expect ')' after expression."
        )

        return processor, expr.Grouping(individual_expression)

    raise error(processor, peek(processor), "Expect expression.")


def match(
    processor: Parser, token_types: List[scanner.TokenType]
) -> Tuple[Parser, bool]:
    """ """
    for token_type in token_types:
        if check(processor, token_type):
            processor, _ = advance(processor)
            return processor, True

    return processor, False


def consume(
    processor: Parser, token_type: scanner.TokenType, message: str
) -> Tuple[Parser, scanner.Token]:
    """ """
    if check(processor, token_type):
        return advance(processor)

    raise error(processor, peek(processor), message)


def advance(processor: Parser) -> Tuple[Parser, scanner.Token]:
    """ """
    if not is_at_end(processor):
        processor.current += 1

    return processor, previous(processor)


def check(processor: Parser, token_type: scanner.TokenType) -> bool:
    """ """
    if is_at_end(processor):
        return False

    return peek(processor).token_type == token_type


def peek(processor: Parser) -> scanner.Token:
    """ """
    return processor.tokens[processor.current]


def previous(processor: Parser) -> scanner.Token:
    """ """
    return processor.tokens[processor.current - 1]


def is_at_end(processor: Parser) -> bool:
    """ """
    return peek(processor).token_type == scanner.TokenType.EOF


def error(processor: Parser, token: scanner.Token, message: str) -> ParseError:
    """ """
    print(
        f"\033[91mError at TokenType.{token.token_type.name} in line {token.line}: {message}\033[0m"
    )
    return ParseError()
