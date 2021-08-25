from typing import List

import compiler
import parser
import scanner
import vm


def source_to_result(source: str) -> List[str]:
    """ """
    searcher = scanner.init_scanner(source=source)
    tokens = scanner.scan(searcher)
    processor = parser.init_parser(tokens=tokens)
    statements = parser.parse(processor)
    composer = compiler.init_compiler(statements=statements)
    bytecode = compiler.compile(composer)
    emulator = vm.init_vm(bytecode=bytecode)
    return vm.run(emulator)


def test_run() -> None:
    """ """
    result = source_to_result(source="print 1 * (2 + 3);")
    assert len(result) == 1

    assert result[0] == "5"
