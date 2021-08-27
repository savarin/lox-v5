from typing import List, Tuple

import compiler
import parser
import scanner


def source_to_bytecode(source: str) -> Tuple[List[compiler.Byte], compiler.Values]:
    """ """
    searcher = scanner.init_scanner(source=source)
    tokens = scanner.scan(searcher)
    processor = parser.init_parser(tokens=tokens)
    statements = parser.parse(processor)
    composer = compiler.init_compiler(statements=statements)
    return compiler.compile(composer)


def test_compile_expression() -> None:
    """ """
    bytecode, values = source_to_bytecode(source="print 1 * (2 + 3);")
    assert len(bytecode) == 9
    assert values.value_count == 3

    assert bytecode[0] == compiler.OpCode.OP_CONSTANT
    assert bytecode[1] == 0
    assert bytecode[2] == compiler.OpCode.OP_CONSTANT
    assert bytecode[3] == 1
    assert bytecode[4] == compiler.OpCode.OP_CONSTANT
    assert bytecode[5] == 2
    assert bytecode[6] == compiler.OpCode.OP_ADD
    assert bytecode[7] == compiler.OpCode.OP_MULTIPLY
    assert bytecode[8] == compiler.OpCode.OP_PRINT

    assert values.array[0] == 1
    assert values.array[1] == 2
    assert values.array[2] == 3


def test_compile_assignment() -> None:
    """ """
    bytecode, values = source_to_bytecode(source="var a; print a;")
    assert len(bytecode) == 5
    assert values.value_count == 0

    assert bytecode[0] == compiler.OpCode.OP_CONSTANT
    assert bytecode[1] is None
    assert bytecode[2] == compiler.OpCode.OP_GET
    assert bytecode[3] == 0
    assert bytecode[4] == compiler.OpCode.OP_PRINT

    bytecode, values = source_to_bytecode(source="var a = 1; print a;")
    assert len(bytecode) == 5
    assert values.value_count == 1

    assert bytecode[0] == compiler.OpCode.OP_CONSTANT
    assert bytecode[1] == 0
    assert bytecode[2] == compiler.OpCode.OP_GET
    assert bytecode[3] == 0
    assert bytecode[4] == compiler.OpCode.OP_PRINT

    assert values.array[0] == 1

    bytecode, values = source_to_bytecode(source="var a = 1; a = 2; print a + 3;")
    assert len(bytecode) == 13
    assert values.value_count == 3

    assert bytecode[0] == compiler.OpCode.OP_CONSTANT
    assert bytecode[1] == 0
    assert bytecode[2] == compiler.OpCode.OP_CONSTANT
    assert bytecode[3] == 1
    assert bytecode[4] == compiler.OpCode.OP_SET
    assert bytecode[5] == 0
    assert bytecode[6] == compiler.OpCode.OP_POP
    assert bytecode[7] == compiler.OpCode.OP_GET
    assert bytecode[8] == 0
    assert bytecode[9] == compiler.OpCode.OP_CONSTANT
    assert bytecode[10] == 2
    assert bytecode[11] == compiler.OpCode.OP_ADD
    assert bytecode[12] == compiler.OpCode.OP_PRINT

    assert values.array[0] == 1
    assert values.array[1] == 2
    assert values.array[2] == 3


def test_compile_scope() -> None:
    """ """
    bytecode, values = source_to_bytecode(
        source="""\
var a = 1;
var b = 2;
var c = 3;
{
    var a = 10;
    var b = 20;
    {
        var a = 100;
        print a;
        print b;
        print c;
    }
    print a;
    print b;
    print c;
}
print a;
print b;
print c;"""
    )
    assert len(bytecode) == 42
    assert values.value_count == 6

    assert bytecode[0] == compiler.OpCode.OP_CONSTANT
    assert bytecode[1] == 0
    assert bytecode[2] == compiler.OpCode.OP_CONSTANT
    assert bytecode[3] == 1
    assert bytecode[4] == compiler.OpCode.OP_CONSTANT
    assert bytecode[5] == 2
    assert bytecode[6] == compiler.OpCode.OP_CONSTANT
    assert bytecode[7] == 3
    assert bytecode[8] == compiler.OpCode.OP_CONSTANT
    assert bytecode[9] == 4
    assert bytecode[10] == compiler.OpCode.OP_CONSTANT
    assert bytecode[11] == 5
    assert bytecode[12] == compiler.OpCode.OP_GET
    assert bytecode[13] == 5
    assert bytecode[14] == compiler.OpCode.OP_PRINT
    assert bytecode[15] == compiler.OpCode.OP_GET
    assert bytecode[16] == 4
    assert bytecode[17] == compiler.OpCode.OP_PRINT
    assert bytecode[18] == compiler.OpCode.OP_GET
    assert bytecode[19] == 2
    assert bytecode[20] == compiler.OpCode.OP_PRINT
    assert bytecode[21] == compiler.OpCode.OP_POP
    assert bytecode[22] == compiler.OpCode.OP_GET
    assert bytecode[23] == 3
    assert bytecode[24] == compiler.OpCode.OP_PRINT
    assert bytecode[25] == compiler.OpCode.OP_GET
    assert bytecode[26] == 4
    assert bytecode[27] == compiler.OpCode.OP_PRINT
    assert bytecode[28] == compiler.OpCode.OP_GET
    assert bytecode[29] == 2
    assert bytecode[30] == compiler.OpCode.OP_PRINT
    assert bytecode[31] == compiler.OpCode.OP_POP
    assert bytecode[32] == compiler.OpCode.OP_POP
    assert bytecode[33] == compiler.OpCode.OP_GET
    assert bytecode[34] == 0
    assert bytecode[35] == compiler.OpCode.OP_PRINT
    assert bytecode[36] == compiler.OpCode.OP_GET
    assert bytecode[37] == 1
    assert bytecode[38] == compiler.OpCode.OP_PRINT
    assert bytecode[39] == compiler.OpCode.OP_GET
    assert bytecode[40] == 2
    assert bytecode[41] == compiler.OpCode.OP_PRINT

    assert values.array[0] == 1
    assert values.array[1] == 2
    assert values.array[2] == 3
    assert values.array[3] == 10
    assert values.array[4] == 20
    assert values.array[5] == 100
