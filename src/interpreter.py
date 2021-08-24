import dataclasses

import expr
import scanner


@dataclasses.dataclass
class Interpreter:
    """ """

    expression: expr.Expr


def init_interpreter(expression: expr.Expr) -> Interpreter:
    """ """
    return Interpreter(expression=expression)


def interpret(inspector: Interpreter) -> int:
    """ """
    return evaluate(inspector.expression)


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
