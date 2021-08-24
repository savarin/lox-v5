import abc
import dataclasses

import scanner


class Expr(abc.ABC):
    """ """

    pass


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
