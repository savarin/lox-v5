from typing import List
import dataclasses

import expr
import scanner
import statem


@dataclasses.dataclass
class Interpreter:
    """ """

    statements: List[statem.Statem]


def init_interpreter(statements: List[statem.Statem]) -> Interpreter:
    """ """
    return Interpreter(statements=statements)


def interpret(inspector: Interpreter) -> List[str]:
    """ """
    result: List[str] = []

    for statement in inspector.statements:
        if isinstance(statement, statem.Expression):
            evaluate(statement.expression)

        elif isinstance(statement, statem.Print):
            result.append(str(evaluate(statement.expression)))

    return result


def evaluate(expression: expr.Expr):
    """ """
    if isinstance(expression, expr.Binary):
        left = evaluate(expression.left)
        right = evaluate(expression.right)
        token_type = expression.operator.token_type

        if token_type == scanner.TokenType.PLUS:
            return left + right

        elif token_type == scanner.TokenType.STAR:
            return left * right

    elif isinstance(expression, expr.Grouping):
        """ """
        return evaluate(expression.expression)

    elif isinstance(expression, expr.Literal):
        return expression.value

    raise Exception
