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


def test_interpret_expression() -> None:
    """ """
    result = source_to_result(source="print 1 * (2 + 3);")
    assert len(result) == 1

    assert result[0] == "5"


def test_interpret_assignment() -> None:
    """ """
    result = source_to_result(source="var a; print a;")
    assert len(result) == 1

    assert result[0] == "nil"

    result = source_to_result(source="var a = 1; print a;")
    assert len(result) == 1

    assert result[0] == "1"

    result = source_to_result(source="var a = 1; a = 2; print a + 3;")
    assert len(result) == 1

    assert result[0] == "5"


def test_interpret_scope() -> None:
    """ """
    result = source_to_result(
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
    assert len(result) == 9

    assert result[0] == "100"
    assert result[1] == "20"
    assert result[2] == "3"
    assert result[3] == "10"
    assert result[4] == "20"
    assert result[5] == "3"
    assert result[6] == "1"
    assert result[7] == "2"
    assert result[8] == "3"
