from typing import Dict, List, Union
import dataclasses
import enum

import expr
import scanner
import statem


Byte = Union["OpCode", int]


class OpCode(enum.Enum):
    """ """

    OP_CONSTANT = "OP_CONSTANT"
    OP_POP = "OP_POP"
    OP_ADD = "OP_ADD"
    OP_SUBTRACT = "OP_SUBTRACT"
    OP_MULTIPLY = "OP_MULTIPLY"
    OP_PRINT = "OP_PRINT"


operator_mapping: Dict[scanner.TokenType, OpCode] = {
    scanner.TokenType.PLUS: OpCode.OP_ADD,
    scanner.TokenType.MINUS: OpCode.OP_SUBTRACT,
    scanner.TokenType.STAR: OpCode.OP_MULTIPLY,
}


@dataclasses.dataclass
class Compiler:
    """ """

    statements: List[statem.Statem]


def init_compiler(statements: List[statem.Statem]) -> Compiler:
    """ """
    return Compiler(statements=statements)


def compile(composer: Compiler) -> List[Byte]:
    """ """
    bytecode: List[Byte] = []

    for statement in composer.statements:
        bytecode += execute(statement)

    return bytecode


def execute(statement: statem.Statem) -> List[Byte]:
    """ """
    bytecode: List[Byte] = []

    if isinstance(statement, statem.Expression):
        bytecode += evaluate(statement.expression)
        bytecode.append(OpCode.OP_POP)

        return bytecode

    elif isinstance(statement, statem.Print):
        bytecode += evaluate(statement.expression)
        bytecode.append(OpCode.OP_PRINT)

        return bytecode

    raise Exception


def evaluate(expression: expr.Expr) -> List[Byte]:
    """ """
    bytecode: List[Byte] = []

    if isinstance(expression, expr.Binary):
        bytecode += evaluate(expression.left)
        bytecode += evaluate(expression.right)

        token_type = operator_mapping[expression.operator.token_type]
        bytecode.append(token_type)

        return bytecode

    elif isinstance(expression, expr.Grouping):
        bytecode += evaluate(expression.expression)

        return bytecode

    elif isinstance(expression, expr.Literal):
        bytecode.append(OpCode.OP_CONSTANT)
        bytecode.append(expression.value)

        return bytecode

    raise Exception
