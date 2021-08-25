import compiler
import parser
import scanner
import vm


def source_to_value(source: str) -> int:
    """ """
    searcher = scanner.init_scanner(source=source)
    tokens = scanner.scan(searcher)
    processor = parser.init_parser(tokens=tokens)
    expression = parser.parse(processor)

    assert expression is not None
    composer = compiler.init_compiler(expression=expression)
    bytecode = compiler.compile(composer)

    emulator = vm.init_vm(bytecode=bytecode)
    return vm.run(emulator)


def test_run() -> None:
    """ """
    assert source_to_value(source="1 * (2 + 3)") == 5
