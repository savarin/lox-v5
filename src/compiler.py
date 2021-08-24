from typing import Dict, List, Union
import dataclasses
import enum

import expr
import scanner


Byte = Union["OpCode", int]


class OpCode(enum.Enum):
    """ """

    OP_CONSTANT = "OP_CONSTANT"
    OP_POP = "OP_POP"
    OP_ADD = "OP_ADD"
    OP_MULTIPLY = "OP_MULTIPLY"


operator_mapping: Dict[scanner.TokenType, OpCode] = {
    scanner.TokenType.PLUS: OpCode.OP_ADD,
    scanner.TokenType.STAR: OpCode.OP_MULTIPLY,
}


@dataclasses.dataclass
class Compiler:
    """ """

    expression: expr.Expr


def init_compiler(expression: expr.Expr) -> Compiler:
    """ """
    return Compiler(expression=expression)


def compile(composer: Compiler) -> List[Union[OpCode, int]]:
    """ """
    bytecode: List[Byte] = []

    def evaluate(expression: expr.Expr):
        """ """
        if isinstance(expression, expr.Binary):
            evaluate(expression.left)
            evaluate(expression.right)

            token_type = operator_mapping[expression.operator.token_type]
            bytecode.append(token_type)

        elif isinstance(expression, expr.Grouping):
            evaluate(expression.expression)

        elif isinstance(expression, expr.Literal):
            bytecode.append(OpCode.OP_CONSTANT)
            bytecode.append(expression.value)

    evaluate(composer.expression)
    return bytecode
