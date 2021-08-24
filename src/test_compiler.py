from typing import List

import compiler
import parser
import scanner


def source_to_bytecode(source: str) -> List[compiler.Byte]:
    """ """
    searcher = scanner.init_scanner(source=source)
    tokens = scanner.scan(searcher)
    processor = parser.init_parser(tokens=tokens)
    expression = parser.parse(processor)

    assert expression is not None
    composer = compiler.init_compiler(expression=expression)

    return compiler.compile(composer)


def test_compile() -> None:
    """ """
    bytecode = source_to_bytecode(source="1 * (2 + 3)")

    assert bytecode[0] == compiler.OpCode.OP_CONSTANT
    assert bytecode[1] == 1
    assert bytecode[2] == compiler.OpCode.OP_CONSTANT
    assert bytecode[3] == 2
    assert bytecode[4] == compiler.OpCode.OP_CONSTANT
    assert bytecode[5] == 3
    assert bytecode[6] == compiler.OpCode.OP_ADD
    assert bytecode[7] == compiler.OpCode.OP_MULTIPLY
