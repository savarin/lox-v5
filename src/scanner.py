from typing import Dict, List, Optional, Tuple
import dataclasses
import enum


class TokenType(enum.Enum):
    """ """

    # Single-character tokens.
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"

    # One or two character tokens.
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"

    # Literals.
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"

    # Keywords
    ELSE = "ELSE"
    FUN = "FUN"
    IF = "IF"
    VAR = "VAR"
    PRINT = "PRINT"
    RETURN = "RETURN"

    EOF = "EOF"


keywords: Dict[str, TokenType] = {
    "else": TokenType.ELSE,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "var": TokenType.VAR,
}


@dataclasses.dataclass
class Token:
    """ """

    token_type: TokenType
    lexeme: str
    literal: Optional[int]
    line: int


@dataclasses.dataclass
class Scanner:
    """ """

    source: str
    tokens: Optional[List[Token]]
    start: int
    current: int
    line: int


def init_scanner(source: str) -> Scanner:
    """ """
    tokens: Optional[List[Token]] = []
    return Scanner(source=source, tokens=tokens, start=0, current=0, line=1)


def scan(searcher: Scanner) -> List[Token]:
    """ """
    while not is_at_end(searcher):
        searcher.start = searcher.current
        searcher = scan_token(searcher)

    assert searcher.tokens is not None
    searcher.tokens.append(Token(TokenType.EOF, "", None, searcher.line))

    return searcher.tokens


def scan_token(searcher: Scanner) -> Scanner:
    """ """
    searcher, character = advance(searcher)

    if character == "(":
        searcher = add_token(searcher, TokenType.LEFT_PAREN)
    elif character == ")":
        searcher = add_token(searcher, TokenType.RIGHT_PAREN)
    elif character == "{":
        searcher = add_token(searcher, TokenType.LEFT_BRACE)
    elif character == "}":
        searcher = add_token(searcher, TokenType.RIGHT_BRACE)
    elif character == ",":
        searcher = add_token(searcher, TokenType.COMMA)
    elif character == "+":
        searcher = add_token(searcher, TokenType.PLUS)
    elif character == "-":
        searcher = add_token(searcher, TokenType.MINUS)
    elif character == "*":
        searcher = add_token(searcher, TokenType.STAR)
    elif character == ";":
        searcher = add_token(searcher, TokenType.SEMICOLON)

    elif character == "=":
        searcher = add_token(
            searcher, TokenType.EQUAL_EQUAL if match(searcher, "=") else TokenType.EQUAL
        )

    elif character == "\n":
        searcher.line += 1
    elif character == " ":
        pass

    elif is_digit(character):
        searcher = number(searcher)
    elif is_alpha(character):
        searcher = identifier(searcher)

    else:
        print(f"\033[91mError in line {searcher.line}: Unexpected character\033[0m")
        raise Exception

    return searcher


def add_token(
    searcher: Scanner, token_type: TokenType, literal: Optional[int] = None
) -> Scanner:
    """ """
    text = searcher.source[searcher.start : searcher.current]

    assert searcher.tokens is not None
    searcher.tokens.append(Token(token_type, text, literal, searcher.line))

    return searcher


def advance(searcher: Scanner) -> Tuple[Scanner, str]:
    """ """
    character = searcher.source[searcher.current]
    searcher.current += 1

    return searcher, character


def peek(searcher: Scanner) -> str:
    """ """
    if is_at_end(searcher):
        return "\0"

    return searcher.source[searcher.current]


def match(searcher: Scanner, expected: str) -> bool:
    """ """
    if is_at_end(searcher):
        return False

    if searcher.source[searcher.current] != expected:
        return False

    searcher.current += 1
    return True


def identifier(searcher: Scanner) -> Scanner:
    """ """
    while is_alpha_numeric(peek(searcher)):
        searcher, _ = advance(searcher)

    text = searcher.source[searcher.start : searcher.current]
    token_type = keywords.get(text, None)

    if token_type is None:
        token_type = TokenType.IDENTIFIER

    return add_token(searcher, token_type)


def number(searcher: Scanner) -> Scanner:
    """ """
    while is_digit(peek(searcher)):
        searcher, _ = advance(searcher)

    return add_token(
        searcher,
        TokenType.NUMBER,
        int(searcher.source[searcher.start : searcher.current]),
    )


def is_alpha_numeric(character: str) -> bool:
    """ """
    return is_alpha(character) or is_digit(character)


def is_alpha(character: str) -> bool:
    """ """
    return (
        (character >= "a" and character <= "z")
        or (character >= "A" and character <= "Z")
        or character == "_"
    )


def is_digit(character: str) -> bool:
    """ """
    return character >= "0" and character <= "9"


def is_at_end(searcher: Scanner) -> bool:
    """ """
    return searcher.current == len(searcher.source)
