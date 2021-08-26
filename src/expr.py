from typing import List
import abc
import dataclasses

import scanner


class Expr(abc.ABC):
    """ """

    pass


@dataclasses.dataclass
class Assign(Expr):
    """ """

    name: scanner.Token
    value: Expr


@dataclasses.dataclass
class Call(Expr):
    """ """

    callee: Expr
    paren: scanner.Token
    arguments: List[Expr]


@dataclasses.dataclass
class Binary(Expr):
    """ """

    left: Expr
    operator: scanner.Token
    right: Expr


@dataclasses.dataclass
class Grouping(Expr):
    """ """

    expression: Expr


@dataclasses.dataclass
class Literal(Expr):
    """ """

    value: int


@dataclasses.dataclass
class Variable(Expr):
    """ """

    name: scanner.Token
