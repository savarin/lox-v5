import interpreter
import parser
import scanner


def source_to_value(source: str) -> int:
    """ """
    searcher = scanner.init_scanner(source=source)
    tokens = scanner.scan(searcher)
    processor = parser.init_parser(tokens=tokens)
    expression = parser.parse(processor)

    assert expression is not None
    inspector = interpreter.init_interpreter(expression=expression)

    return interpreter.interpret(inspector)


def test_interpret() -> None:
    """ """
    assert source_to_value(source="1 * (2 + 3)") == 5
