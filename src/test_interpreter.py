from typing import List

import interpreter
import parser
import scanner


def source_to_result(source: str) -> List[str]:
    """ """
    searcher = scanner.init_scanner(source=source)
    tokens = scanner.scan(searcher)
    processor = parser.init_parser(tokens=tokens)
    statements = parser.parse(processor)
    inspector = interpreter.init_interpreter(statements=statements)
    return interpreter.interpret(inspector)


def test_interpret() -> None:
    """ """
    result = source_to_result(source="print 1 * (2 + 3);")
    assert len(result) == 1

    assert result[0] == "5"
