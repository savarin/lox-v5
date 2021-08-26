from typing import List

import scanner


def source_to_tokens(source: str) -> List[scanner.Token]:
    """ """
    searcher = scanner.init_scanner(source=source)
    return scanner.scan(searcher)


def test_scan_expression() -> None:
    """ """
    tokens = source_to_tokens(source="1 * (2 + 3);")
    assert len(tokens) == 9

    assert tokens[0] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="1", literal=1, line=1
    )
    assert tokens[1] == scanner.Token(
        token_type=scanner.TokenType.STAR, lexeme="*", literal=None, line=1
    )
    assert tokens[2] == scanner.Token(
        token_type=scanner.TokenType.LEFT_PAREN, lexeme="(", literal=None, line=1
    )
    assert tokens[3] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="2", literal=2, line=1
    )
    assert tokens[4] == scanner.Token(
        token_type=scanner.TokenType.PLUS, lexeme="+", literal=None, line=1
    )
    assert tokens[5] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="3", literal=3, line=1
    )
    assert tokens[6] == scanner.Token(
        token_type=scanner.TokenType.RIGHT_PAREN, lexeme=")", literal=None, line=1
    )
    assert tokens[7] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=1
    )
    assert tokens[8] == scanner.Token(
        token_type=scanner.TokenType.EOF, lexeme="", literal=None, line=1
    )


def test_scan_assignment() -> None:
    """ """
    tokens = source_to_tokens(source="var a; print a;")
    assert len(tokens) == 7

    assert tokens[0] == scanner.Token(
        token_type=scanner.TokenType.VAR, lexeme="var", literal=None, line=1
    )
    assert tokens[1] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=1
    )
    assert tokens[2] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=1
    )
    assert tokens[3] == scanner.Token(
        token_type=scanner.TokenType.PRINT, lexeme="print", literal=None, line=1
    )
    assert tokens[4] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=1
    )
    assert tokens[5] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=1
    )
    assert tokens[6] == scanner.Token(
        token_type=scanner.TokenType.EOF, lexeme="", literal=None, line=1
    )

    tokens = source_to_tokens(source="var a = 1; print a;")
    assert len(tokens) == 9

    assert tokens[0] == scanner.Token(
        token_type=scanner.TokenType.VAR, lexeme="var", literal=None, line=1
    )
    assert tokens[1] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=1
    )
    assert tokens[2] == scanner.Token(
        token_type=scanner.TokenType.EQUAL, lexeme="=", literal=None, line=1
    )
    assert tokens[3] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="1", literal=1, line=1
    )
    assert tokens[4] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=1
    )
    assert tokens[5] == scanner.Token(
        token_type=scanner.TokenType.PRINT, lexeme="print", literal=None, line=1
    )
    assert tokens[6] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=1
    )
    assert tokens[7] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=1
    )
    assert tokens[8] == scanner.Token(
        token_type=scanner.TokenType.EOF, lexeme="", literal=None, line=1
    )

    tokens = source_to_tokens(source="var a = 1; a = 2; print a + 3;")
    assert len(tokens) == 15

    assert tokens[0] == scanner.Token(
        token_type=scanner.TokenType.VAR, lexeme="var", literal=None, line=1
    )
    assert tokens[1] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=1
    )
    assert tokens[2] == scanner.Token(
        token_type=scanner.TokenType.EQUAL, lexeme="=", literal=None, line=1
    )
    assert tokens[3] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="1", literal=1, line=1
    )
    assert tokens[4] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=1
    )
    assert tokens[5] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=1
    )
    assert tokens[6] == scanner.Token(
        token_type=scanner.TokenType.EQUAL, lexeme="=", literal=None, line=1
    )
    assert tokens[7] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="2", literal=2, line=1
    )
    assert tokens[8] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=1
    )
    assert tokens[9] == scanner.Token(
        token_type=scanner.TokenType.PRINT, lexeme="print", literal=None, line=1
    )
    assert tokens[10] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=1
    )
    assert tokens[11] == scanner.Token(
        token_type=scanner.TokenType.PLUS, lexeme="+", literal=None, line=1
    )
    assert tokens[12] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="3", literal=3, line=1
    )
    assert tokens[13] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=1
    )
    assert tokens[14] == scanner.Token(
        token_type=scanner.TokenType.EOF, lexeme="", literal=None, line=1
    )


def test_scan_scope() -> None:
    """ """
    tokens = source_to_tokens(
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
    assert len(tokens) == 62

    assert tokens[0] == scanner.Token(
        token_type=scanner.TokenType.VAR, lexeme="var", literal=None, line=1
    )
    assert tokens[1] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=1
    )
    assert tokens[2] == scanner.Token(
        token_type=scanner.TokenType.EQUAL, lexeme="=", literal=None, line=1
    )
    assert tokens[3] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="1", literal=1, line=1
    )
    assert tokens[4] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=1
    )
    assert tokens[5] == scanner.Token(
        token_type=scanner.TokenType.VAR, lexeme="var", literal=None, line=2
    )
    assert tokens[6] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="b", literal=None, line=2
    )
    assert tokens[7] == scanner.Token(
        token_type=scanner.TokenType.EQUAL, lexeme="=", literal=None, line=2
    )
    assert tokens[8] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="2", literal=2, line=2
    )
    assert tokens[9] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=2
    )
    assert tokens[10] == scanner.Token(
        token_type=scanner.TokenType.VAR, lexeme="var", literal=None, line=3
    )
    assert tokens[11] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="c", literal=None, line=3
    )
    assert tokens[12] == scanner.Token(
        token_type=scanner.TokenType.EQUAL, lexeme="=", literal=None, line=3
    )
    assert tokens[13] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="3", literal=3, line=3
    )
    assert tokens[14] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=3
    )

    assert tokens[15] == scanner.Token(
        token_type=scanner.TokenType.LEFT_BRACE, lexeme="{", literal=None, line=4
    )

    assert tokens[16] == scanner.Token(
        token_type=scanner.TokenType.VAR, lexeme="var", literal=None, line=5
    )
    assert tokens[17] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=5
    )
    assert tokens[18] == scanner.Token(
        token_type=scanner.TokenType.EQUAL, lexeme="=", literal=None, line=5
    )
    assert tokens[19] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="10", literal=10, line=5
    )
    assert tokens[20] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=5
    )
    assert tokens[21] == scanner.Token(
        token_type=scanner.TokenType.VAR, lexeme="var", literal=None, line=6
    )
    assert tokens[22] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="b", literal=None, line=6
    )
    assert tokens[23] == scanner.Token(
        token_type=scanner.TokenType.EQUAL, lexeme="=", literal=None, line=6
    )
    assert tokens[24] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="20", literal=20, line=6
    )
    assert tokens[25] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=6
    )

    assert tokens[26] == scanner.Token(
        token_type=scanner.TokenType.LEFT_BRACE, lexeme="{", literal=None, line=7
    )

    assert tokens[27] == scanner.Token(
        token_type=scanner.TokenType.VAR, lexeme="var", literal=None, line=8
    )
    assert tokens[28] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=8
    )
    assert tokens[29] == scanner.Token(
        token_type=scanner.TokenType.EQUAL, lexeme="=", literal=None, line=8
    )
    assert tokens[30] == scanner.Token(
        token_type=scanner.TokenType.NUMBER, lexeme="100", literal=100, line=8
    )
    assert tokens[31] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=8
    )
    assert tokens[32] == scanner.Token(
        token_type=scanner.TokenType.PRINT, lexeme="print", literal=None, line=9
    )
    assert tokens[33] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=9
    )
    assert tokens[34] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=9
    )
    assert tokens[35] == scanner.Token(
        token_type=scanner.TokenType.PRINT, lexeme="print", literal=None, line=10
    )
    assert tokens[36] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="b", literal=None, line=10
    )
    assert tokens[37] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=10
    )
    assert tokens[38] == scanner.Token(
        token_type=scanner.TokenType.PRINT, lexeme="print", literal=None, line=11
    )
    assert tokens[39] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="c", literal=None, line=11
    )
    assert tokens[40] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=11
    )

    assert tokens[41] == scanner.Token(
        token_type=scanner.TokenType.RIGHT_BRACE, lexeme="}", literal=None, line=12
    )

    assert tokens[42] == scanner.Token(
        token_type=scanner.TokenType.PRINT, lexeme="print", literal=None, line=13
    )
    assert tokens[43] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=13
    )
    assert tokens[44] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=13
    )
    assert tokens[45] == scanner.Token(
        token_type=scanner.TokenType.PRINT, lexeme="print", literal=None, line=14
    )
    assert tokens[46] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="b", literal=None, line=14
    )
    assert tokens[47] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=14
    )
    assert tokens[48] == scanner.Token(
        token_type=scanner.TokenType.PRINT, lexeme="print", literal=None, line=15
    )
    assert tokens[49] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="c", literal=None, line=15
    )
    assert tokens[50] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=15
    )

    assert tokens[51] == scanner.Token(
        token_type=scanner.TokenType.RIGHT_BRACE, lexeme="}", literal=None, line=16
    )

    assert tokens[52] == scanner.Token(
        token_type=scanner.TokenType.PRINT, lexeme="print", literal=None, line=17
    )
    assert tokens[53] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="a", literal=None, line=17
    )
    assert tokens[54] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=17
    )
    assert tokens[55] == scanner.Token(
        token_type=scanner.TokenType.PRINT, lexeme="print", literal=None, line=18
    )
    assert tokens[56] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="b", literal=None, line=18
    )
    assert tokens[57] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=18
    )
    assert tokens[58] == scanner.Token(
        token_type=scanner.TokenType.PRINT, lexeme="print", literal=None, line=19
    )
    assert tokens[59] == scanner.Token(
        token_type=scanner.TokenType.IDENTIFIER, lexeme="c", literal=None, line=19
    )
    assert tokens[60] == scanner.Token(
        token_type=scanner.TokenType.SEMICOLON, lexeme=";", literal=None, line=19
    )
    assert tokens[61] == scanner.Token(
        token_type=scanner.TokenType.EOF, lexeme="", literal=None, line=19
    )
