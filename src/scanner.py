from typing import List, Optional, Tuple
import dataclasses
import enum


class TokenType(enum.Enum):
    """ """

    # Single-character tokens.
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    PLUS = "PLUS"
    STAR = "STAR"

    # Literals.
    NUMBER = "NUMBER"

    EOF = "EOF"


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
    elif character == "+":
        searcher = add_token(searcher, TokenType.PLUS)
    elif character == "*":
        searcher = add_token(searcher, TokenType.STAR)

    elif character == "\n":
        searcher.line += 1
    elif character == " ":
        pass

    elif is_digit(character):
        searcher = number(searcher)

    else:
        print(f"\033[91mError in line {searcher.line}: Unexpected character\033[0m")
        raise Exception

    return searcher


def advance(searcher: Scanner) -> Tuple[Scanner, str]:
    """ """
    character = searcher.source[searcher.current]
    searcher.current += 1

    return searcher, character


def add_token(
    searcher: Scanner, token_type: TokenType, literal: Optional[int] = None
) -> Scanner:
    """ """
    text = searcher.source[searcher.start : searcher.current]

    assert searcher.tokens is not None
    searcher.tokens.append(Token(token_type, text, literal, searcher.line))

    return searcher


def is_digit(character: str) -> bool:
    """ """
    return character >= "0" and character <= "9"


def number(searcher: Scanner) -> Scanner:
    """ """
    while is_digit(peek(searcher)):
        searcher, _ = advance(searcher)

    return add_token(
        searcher,
        TokenType.NUMBER,
        int(searcher.source[searcher.start : searcher.current]),
    )


def peek(searcher: Scanner) -> str:
    """ """
    if is_at_end(searcher):
        return "\0"

    return searcher.source[searcher.current]


def is_at_end(searcher: Scanner) -> bool:
    """ """
    return searcher.current >= len(searcher.source)
