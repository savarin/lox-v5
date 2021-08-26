from typing import Dict, List, Optional, Tuple, Union
import dataclasses

import expr
import scanner
import statem


@dataclasses.dataclass
class Environment:
    """ """

    enclosing: Optional["Environment"]
    values: Dict[str, Union[int, statem.Function, None]]


def init_environment(enclosing: Optional["Environment"] = None) -> Environment:
    """ """
    values: Dict[str, Union[int, statem.Function, None]] = {}

    if enclosing is not None:
        individual_enclosing = enclosing.enclosing
        individual_values = enclosing.values.copy()

        enclosing = Environment(
            enclosing=individual_enclosing, values=individual_values
        )

    return Environment(enclosing=enclosing, values=values)


def define(
    environment: Environment, name: str, value: Union[int, statem.Function, None]
) -> Environment:
    """ """
    environment.values[name] = value
    return environment


def get(
    environment: Environment, token: scanner.Token
) -> Union[int, statem.Function, None]:
    """ """
    lexeme = token.lexeme

    if lexeme in environment.values:
        return environment.values[lexeme]

    if environment.enclosing is not None:
        return get(environment.enclosing, token)

    raise Exception


def assign(
    environment: Environment,
    token: scanner.Token,
    value: Union[int, statem.Function, None],
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
class Return(Exception):
    """ """

    value: Union[int, bool, statem.Function, List[str], None]


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

    elif isinstance(statement, statem.Function):
        inspector.environment = define(
            inspector.environment, statement.name.lexeme, statement
        )
        return inspector, []

    elif isinstance(statement, statem.Expression):
        result = evaluate(inspector, statement.expression)

        if result is not None and isinstance(result, list):
            return inspector, result

        return inspector, []

    elif isinstance(statement, statem.If):
        if evaluate(inspector, statement.condition):
            return execute(inspector, statement.then_branch)

        elif statement.else_branch is not None:
            return execute(inspector, statement.else_branch)

        return inspector, []

    elif isinstance(statement, statem.Print):
        result = evaluate(inspector, statement.expression)
        return inspector, [str(result or "nil")]

    elif isinstance(statement, statem.Return):
        value = None

        if statement.value is not None:
            value = evaluate(inspector, statement.value)

        raise Return(value)

    elif isinstance(statement, statem.Var):
        value = None

        if statement.initializer is not None:
            value = evaluate(inspector, statement.initializer)

        assert (
            isinstance(value, int)
            or isinstance(value, statem.Function)
            or value is None
        )
        inspector.environment = define(
            inspector.environment, statement.name.lexeme, value
        )

        return inspector, []

    raise Exception


def execute_block(
    inspector: Interpreter, statements: List[statem.Statem], environment: Environment
) -> Tuple[Interpreter, List[str]]:
    """ """
    result: List[str] = []
    previous = inspector.environment

    try:
        inspector.environment = environment

        for statement in statements:
            inspector, individual_result = execute(inspector, statement)
            result += individual_result

    finally:
        inspector.environment = previous

    return inspector, result


def evaluate(
    inspector: Interpreter, expression: expr.Expr
) -> Union[int, bool, statem.Function, List[str], None]:
    """ """
    if isinstance(expression, expr.Assign):
        value = evaluate(inspector, expression.value)

        assert (
            isinstance(value, int)
            or isinstance(value, statem.Function)
            or value is None
        )
        inspector.environment = assign(inspector.environment, expression.name, value)

        return None

    if isinstance(expression, expr.Binary):
        left = evaluate(inspector, expression.left)
        right = evaluate(inspector, expression.right)
        token_type = expression.operator.token_type

        if token_type == scanner.TokenType.EQUAL_EQUAL:
            if left is None and right is None:
                return True

            elif left is None or right is None:
                return False

            return left == right

        assert isinstance(left, int) and isinstance(right, int)

        if token_type == scanner.TokenType.PLUS:
            return left + right

        elif token_type == scanner.TokenType.MINUS:
            return left - right

        elif token_type == scanner.TokenType.STAR:
            return left * right

    elif isinstance(expression, expr.Call):
        arguments: List[int] = []
        callee = evaluate(inspector, expression.callee)

        for argument in expression.arguments:
            individual_argument = evaluate(inspector, argument)

            assert isinstance(individual_argument, int)
            arguments.append(individual_argument)

        assert isinstance(callee, statem.Function)
        return call(inspector, callee, arguments)

    elif isinstance(expression, expr.Grouping):
        """ """
        return evaluate(inspector, expression.expression)

    elif isinstance(expression, expr.Literal):
        return expression.value

    elif isinstance(expression, expr.Variable):
        return get(inspector.environment, expression.name)

    raise Exception


def call(
    inspector: Interpreter, function: statem.Function, arguments: List[int]
) -> Union[int, bool, statem.Function, List[str], None]:
    """ """
    environment = init_environment(inspector.environment)

    for i, parameter in enumerate(function.parameters):
        environment = define(environment, parameter.lexeme, arguments[i])

    try:
        _, result = execute_block(inspector, function.body, environment)
    except Return as return_value:
        return return_value.value

    return result
