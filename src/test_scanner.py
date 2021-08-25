from typing import List

import scanner


def source_to_tokens(source: str) -> List[scanner.Token]:
    """ """
    searcher = scanner.init_scanner(source=source)
    return scanner.scan(searcher)


def test_scan() -> None:
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
