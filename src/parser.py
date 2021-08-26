from typing import List, Tuple, Optional
import dataclasses

import expr
import scanner
import statem


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


def parse(processor: Parser) -> List[statem.Statem]:
    """ """
    statements: List[statem.Statem] = []

    while not is_at_end(processor):
        processor, individual_statement = declaration(processor)

        if individual_statement is not None:
            statements.append(individual_statement)

    return statements


def declaration(processor: Parser) -> Tuple[Parser, Optional[statem.Statem]]:
    """ """
    try:
        processor, is_match = match(processor, [scanner.TokenType.FUN])

        if is_match:
            return function(processor)

        processor, is_match = match(processor, [scanner.TokenType.VAR])

        if is_match:
            return var_declaration(processor)

        return statement(processor)

    except ParseError:
        return synchronize(processor), None


def function(processor: Parser) -> Tuple[Parser, statem.Statem]:
    """ """
    processor, name = consume(
        processor, scanner.TokenType.IDENTIFIER, "Expect function name."
    )

    processor, _ = consume(
        processor, scanner.TokenType.LEFT_PAREN, "Expect '(' after function name."
    )

    parameters: List[scanner.Token] = []

    if not check(processor, scanner.TokenType.RIGHT_PAREN):
        while True:
            processor, parameter = consume(
                processor, scanner.TokenType.IDENTIFIER, "Expect parameter name."
            )

            parameters.append(parameter)

            processor, is_match = match(processor, [scanner.TokenType.COMMA])

            if not is_match:
                break

    processor, _ = consume(
        processor, scanner.TokenType.RIGHT_PAREN, "Expect ')' after parameters."
    )

    processor, _ = consume(
        processor, scanner.TokenType.LEFT_BRACE, "Expect '{' before body."
    )

    processor, body = block(processor)
    return processor, statem.Function(name, parameters, body)


def var_declaration(processor: Parser) -> Tuple[Parser, statem.Statem]:
    """ """
    processor, name = consume(
        processor, scanner.TokenType.IDENTIFIER, "Expect variable name."
    )

    initializer = None
    processor, is_match = match(processor, [scanner.TokenType.EQUAL])

    if is_match:
        processor, initializer = expression(processor)

    processor, _ = consume(
        processor, scanner.TokenType.SEMICOLON, "Expect ';' after variable declaration."
    )

    return processor, statem.Var(name, initializer)


def statement(processor: Parser) -> Tuple[Parser, statem.Statem]:
    """ """
    processor, is_match = match(processor, [scanner.TokenType.IF])

    if is_match:
        return if_statement(processor)

    processor, is_match = match(processor, [scanner.TokenType.PRINT])

    if is_match:
        return print_statement(processor)

    processor, is_match = match(processor, [scanner.TokenType.RETURN])

    if is_match:
        return return_statement(processor)

    processor, is_match = match(processor, [scanner.TokenType.LEFT_BRACE])

    if is_match:
        processor, statements = block(processor)
        return processor, statem.Block(statements)

    return expression_statement(processor)


def if_statement(processor: Parser) -> Tuple[Parser, statem.Statem]:
    """ """
    processor, _ = consume(
        processor, scanner.TokenType.LEFT_PAREN, "Expect '(' after 'if'."
    )

    processor, condition = expression(processor)

    processor, _ = consume(
        processor, scanner.TokenType.RIGHT_PAREN, "Expect ')' after if condition."
    )

    processor, then_branch = statement(processor)

    else_branch = None

    processor, is_match = match(processor, [scanner.TokenType.ELSE])

    if is_match:
        processor, else_branch = statement(processor)

    return processor, statem.If(condition, then_branch, else_branch)


def print_statement(processor: Parser) -> Tuple[Parser, statem.Statem]:
    """ """
    processor, individual_expression = expression(processor)
    processor, _ = consume(
        processor, scanner.TokenType.SEMICOLON, "Expect ';' after print statement."
    )

    return processor, statem.Print(individual_expression)


def return_statement(processor: Parser) -> Tuple[Parser, statem.Return]:
    """ """
    keyword = previous(processor)
    value = None

    if not check(processor, scanner.TokenType.SEMICOLON):
        processor, value = expression(processor)

    processor, _ = consume(
        processor, scanner.TokenType.SEMICOLON, "Expect ';' after return value."
    )

    return processor, statem.Return(keyword, value)


def block(processor: Parser) -> Tuple[Parser, List[statem.Statem]]:
    """ """
    statements: List[statem.Statem] = []

    while not check(processor, scanner.TokenType.RIGHT_BRACE) and not is_at_end(
        processor
    ):
        processor, individual_statement = declaration(processor)

        if individual_statement is not None:
            statements.append(individual_statement)

    processor, _ = consume(
        processor, scanner.TokenType.RIGHT_BRACE, "Expect '}' after block."
    )

    return processor, statements


def expression_statement(processor: Parser) -> Tuple[Parser, statem.Statem]:
    """ """
    processor, individual_expression = expression(processor)
    processor, _ = consume(
        processor, scanner.TokenType.SEMICOLON, "Expect ';' after expression."
    )

    return processor, statem.Expression(individual_expression)


def expression(processor: Parser) -> Tuple[Parser, expr.Expr]:
    """ """
    return assignment(processor)


def assignment(processor: Parser) -> Tuple[Parser, expr.Expr]:
    """ """
    processor, equality_expression = equality(processor)
    processor, is_match = match(processor, [scanner.TokenType.EQUAL])

    if is_match:
        equals = previous(processor)
        processor, value = assignment(processor)

        if isinstance(equality_expression, expr.Variable):
            name = equality_expression.name
            return processor, expr.Assign(name, value)

        raise error(processor, equals, "Invalid assignment target.")

    return processor, equality_expression


def equality(processor: Parser) -> Tuple[Parser, expr.Expr]:
    """ """
    processor, term_expression = term(processor)

    while True:
        processor, is_match = match(processor, [scanner.TokenType.EQUAL_EQUAL])

        if not is_match:
            break

        operator = previous(processor)
        processor, right = term(processor)
        term_expression = expr.Binary(term_expression, operator, right)

    return processor, term_expression


def term(processor: Parser) -> Tuple[Parser, expr.Expr]:
    """ """
    processor, factor_expression = factor(processor)

    while True:
        processor, is_match = match(
            processor, [scanner.TokenType.PLUS, scanner.TokenType.MINUS]
        )

        if not is_match:
            break

        operator = previous(processor)
        processor, right = factor(processor)
        factor_expression = expr.Binary(factor_expression, operator, right)

    return processor, factor_expression


def factor(processor: Parser) -> Tuple[Parser, expr.Expr]:
    """ """
    processor, call_expression = call(processor)

    while True:
        processor, is_match = match(processor, [scanner.TokenType.STAR])

        if not is_match:
            break

        operator = previous(processor)
        processor, right = call(processor)
        call_expression = expr.Binary(call_expression, operator, right)

    return processor, call_expression


def call(processor: Parser) -> Tuple[Parser, expr.Expr]:
    """ """
    processor, primary_expression = primary(processor)

    while True:
        processor, is_match = match(processor, [scanner.TokenType.LEFT_PAREN])

        if is_match:
            processor, primary_expression = finish_call(processor, primary_expression)
        else:
            break

    return processor, primary_expression


def finish_call(processor: Parser, callee: expr.Expr) -> Tuple[Parser, expr.Expr]:
    """ """
    arguments: List[expr.Expr] = []

    if not check(processor, scanner.TokenType.RIGHT_PAREN):
        while True:
            processor, individual_expression = expression(processor)
            arguments.append(individual_expression)

            processor, is_match = match(processor, [scanner.TokenType.COMMA])

            if not is_match:
                break

    processor, paren = consume(
        processor, scanner.TokenType.RIGHT_PAREN, "Expect ')' after arguments."
    )

    return processor, expr.Call(callee, paren, arguments)


def primary(processor: Parser) -> Tuple[Parser, expr.Expr]:
    """ """
    processor, is_match = match(processor, [scanner.TokenType.NUMBER])

    if is_match:
        value = previous(processor).literal

        assert value is not None
        return processor, expr.Literal(value)

    processor, is_match = match(processor, [scanner.TokenType.IDENTIFIER])

    if is_match:
        return processor, expr.Variable(previous(processor))

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


def error(processor: Parser, token: scanner.Token, message: str) -> ParseError:
    """ """
    print(
        f"\033[91mError at TokenType.{token.token_type.name} in line {token.line}: {message}\033[0m"
    )
    return ParseError()


def synchronize(processor: Parser) -> Parser:
    """ """
    processor, _ = advance(processor)

    while not is_at_end(processor):
        if previous(processor).token_type == scanner.TokenType.SEMICOLON:
            return processor

        token_type = peek(processor).token_type

        if token_type in [
            scanner.TokenType.IF,
            scanner.TokenType.PRINT,
            scanner.TokenType.VAR,
        ]:
            return processor

        procesor, _ = advance(processor)

    return processor


def is_at_end(processor: Parser) -> bool:
    """ """
    return peek(processor).token_type == scanner.TokenType.EOF
