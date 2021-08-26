from typing import Dict, List, Optional, Tuple
import dataclasses

import expr
import scanner
import statem


@dataclasses.dataclass
class Environment:
    """ """

    enclosing: Optional["Environment"]
    values: Dict[str, Optional[int]]


def init_environment(enclosing: Optional["Environment"] = None) -> Environment:
    """ """
    values: Dict[str, Optional[int]] = {}

    if enclosing is not None:
        individual_enclosing = enclosing.enclosing
        individual_values = enclosing.values.copy()

        enclosing = Environment(
            enclosing=individual_enclosing, values=individual_values
        )

    return Environment(enclosing=enclosing, values=values)


def define(environment: Environment, name: str, value: Optional[int]) -> Environment:
    """ """
    environment.values[name] = value
    return environment


def get(environment: Environment, token: scanner.Token) -> Optional[int]:
    """ """
    lexeme = token.lexeme

    if lexeme in environment.values:
        return environment.values[lexeme]

    if environment.enclosing is not None:
        return get(environment.enclosing, token)

    raise Exception


def assign(
    environment: Environment, token: scanner.Token, value: Optional[int]
) -> Environment:
    """ """
    lexeme = token.lexeme

    if lexeme in environment.values:
        environment.values[lexeme] = value
        return environment

    if environment.enclosing is not None:
        environment.enclosing = assign(environment.enclosing, token, value)
        return environment

    raise Exception


@dataclasses.dataclass
class Interpreter:
    """ """

    statements: List[statem.Statem]
    environment: Environment


def init_interpreter(statements: List[statem.Statem]) -> Interpreter:
    """ """
    environment = init_environment()
    return Interpreter(statements=statements, environment=environment)


def interpret(inspector: Interpreter) -> List[str]:
    """ """
    result: List[str] = []

    for statement in inspector.statements:
        inspector, individual_result = execute(inspector, statement)
        result += individual_result

    return result


def execute(
    inspector: Interpreter, statement: statem.Statem
) -> Tuple[Interpreter, List[str]]:
    """ """
    if isinstance(statement, statem.Block):
        environment = init_environment(inspector.environment)
        return execute_block(inspector, statement.statements, environment)

    elif isinstance(statement, statem.Expression):
        evaluate(inspector, statement.expression)
        return inspector, []

    elif isinstance(statement, statem.Print):
        result = evaluate(inspector, statement.expression) or "nil"
        return inspector, [str(result)]

    elif isinstance(statement, statem.Var):
        value = None

        if statement.initializer is not None:
            value = evaluate(inspector, statement.initializer)

        inspector.environment = define(
            inspector.environment, statement.name.lexeme, value
        )

        return inspector, []

    raise Exception


def execute_block(
    inspector: Interpreter, statements: List[statem.Statem], environment: Environment
) -> Tuple[Interpreter, List[str]]:
    """ """
    previous = inspector.environment

    result: List[str] = []

    try:
        inspector.environment = environment

        for statement in statements:
            inspector, individual_result = execute(inspector, statement)
            result += individual_result

    finally:
        inspector.environment = previous

    return inspector, result


def evaluate(inspector: Interpreter, expression: expr.Expr) -> Optional[int]:
    """ """
    if isinstance(expression, expr.Assign):
        value = evaluate(inspector, expression.value)
        inspector.environment = assign(inspector.environment, expression.name, value)

        return None

    if isinstance(expression, expr.Binary):
        left = evaluate(inspector, expression.left)
        right = evaluate(inspector, expression.right)
        token_type = expression.operator.token_type

        assert left is not None and right is not None

        if token_type == scanner.TokenType.PLUS:
            return left + right

        elif token_type == scanner.TokenType.STAR:
            return left * right

    elif isinstance(expression, expr.Grouping):
        """ """
        return evaluate(inspector, expression.expression)

    elif isinstance(expression, expr.Literal):
        return expression.value

    elif isinstance(expression, expr.Variable):
        return get(inspector.environment, expression.name)

    raise Exception
