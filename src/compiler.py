from typing import Dict, List, Optional, Tuple, Union
import dataclasses
import enum

import expr
import scanner
import statem


INT_COUNT = 8


Byte = Union["OpCode", int, None]


class OpCode(enum.Enum):
    """ """

    OP_CONSTANT = "OP_CONSTANT"
    OP_POP = "OP_POP"
    OP_GET = "OP_GET"
    OP_SET = "OP_SET"
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
class Local:
    """ """

    name: scanner.Token
    depth: int


@dataclasses.dataclass
class Values:
    """ """

    array: List[Optional[int]]
    value_count: int


def init_values() -> Values:
    """ """
    array: List[Optional[int]] = [None] * INT_COUNT
    return Values(array=array, value_count=0)


def write(values: Values, constant: int) -> Tuple[Values, int]:
    """ """
    values.array[values.value_count] = constant
    values.value_count += 1

    return values, values.value_count - 1


@dataclasses.dataclass
class Compiler:
    """ """

    statements: List[statem.Statem]
    array: List[Optional[Local]]
    local_count: int
    scope_depth: int


def init_compiler(statements: List[statem.Statem]) -> Compiler:
    """ """
    array: List[Optional[Local]] = [None] * INT_COUNT
    return Compiler(statements=statements, array=array, local_count=0, scope_depth=0)


def compile(composer: Compiler) -> Tuple[List[Byte], Values]:
    """ """
    bytecode: List[Byte] = []
    values = init_values()

    for statement in composer.statements:
        composer, values, individual_bytecode = execute(composer, values, statement)
        bytecode += individual_bytecode

    return bytecode, values


def execute(
    composer: Compiler, values: Values, statement: statem.Statem
) -> Tuple[Compiler, Values, List[Byte]]:
    """ """
    bytecode: List[Byte] = []

    if isinstance(statement, statem.Block):
        return execute_block(composer, values, statement.statements)

    elif isinstance(statement, statem.Expression):
        values, individual_bytecode = evaluate(composer, values, statement.expression)
        bytecode += individual_bytecode
        bytecode.append(OpCode.OP_POP)

        return composer, values, bytecode

    elif isinstance(statement, statem.Print):
        values, individual_bytecode = evaluate(composer, values, statement.expression)
        bytecode += individual_bytecode
        bytecode.append(OpCode.OP_PRINT)

        return composer, values, bytecode

    elif isinstance(statement, statem.Var):
        value: List[Byte] = [OpCode.OP_CONSTANT, None]

        if statement.initializer is not None:
            values, value = evaluate(composer, values, statement.initializer)

        bytecode += value

        composer.array[composer.local_count] = Local(
            statement.name, composer.scope_depth
        )
        composer.local_count += 1

        return composer, values, bytecode

    raise Exception


def execute_block(
    composer: Compiler, values: Values, statements: List[statem.Statem]
) -> Tuple[Compiler, Values, List[Byte]]:
    """ """
    bytecode: List[Byte] = []

    composer.scope_depth += 1

    for statement in statements:
        composer, values, individual_bytecode = execute(composer, values, statement)
        bytecode += individual_bytecode

    composer.scope_depth -= 1

    while True:
        local = composer.array[composer.local_count - 1]
        assert local is not None

        if composer.local_count == 0 or local.depth <= composer.scope_depth:
            break

        bytecode.append(OpCode.OP_POP)
        composer.local_count -= 1

    return composer, values, bytecode


def evaluate(
    composer: Compiler, values: Values, expression: expr.Expr
) -> Tuple[Values, List[Byte]]:
    """ """
    bytecode: List[Byte] = []

    if isinstance(expression, expr.Assign):
        values, individual_bytecode = evaluate(composer, values, expression.value)
        bytecode += individual_bytecode

        location = resolve_local(composer, expression.name)

        if location is not None:
            bytecode.append(OpCode.OP_SET)
            bytecode.append(location)

            return values, bytecode

    elif isinstance(expression, expr.Binary):
        values, individual_bytecode = evaluate(composer, values, expression.left)
        bytecode += individual_bytecode

        values, individual_bytecode = evaluate(composer, values, expression.right)
        bytecode += individual_bytecode

        token_type = operator_mapping[expression.operator.token_type]
        bytecode.append(token_type)

        return values, bytecode

    elif isinstance(expression, expr.Grouping):
        values, individual_bytecode = evaluate(composer, values, expression.expression)
        bytecode += individual_bytecode

        return values, bytecode

    elif isinstance(expression, expr.Literal):
        values, location = write(values, expression.value)
        bytecode += [OpCode.OP_CONSTANT, location]

        return values, bytecode

    elif isinstance(expression, expr.Variable):
        location = resolve_local(composer, expression.name)

        if location is not None:
            bytecode.append(OpCode.OP_GET)
            bytecode.append(location)

            return values, bytecode

    raise Exception


def resolve_local(composer: Compiler, token: scanner.Token) -> Optional[int]:
    """ """
    for i in range(composer.local_count - 1, -1, -1):
        local = composer.array[i]
        assert local is not None

        if token.lexeme == local.name.lexeme:
            return i

    return None
