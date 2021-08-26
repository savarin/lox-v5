from typing import List

import expr
import parser
import scanner
import statem


def source_to_statements(source: str) -> List[statem.Statem]:
    """ """
    searcher = scanner.init_scanner(source=source)
    tokens = scanner.scan(searcher)
    processor = parser.init_parser(tokens=tokens)
    return parser.parse(processor)


def test_parse_expression() -> None:
    """ """
    statements = source_to_statements(source="1 * (2 + 3);")
    assert len(statements) == 1

    statement = statements[0]
    assert isinstance(statement, statem.Expression)

    expression = statement.expression
    assert isinstance(expression, expr.Binary)
    assert isinstance(expression.left, expr.Literal)
    assert isinstance(expression.right, expr.Grouping)
    assert expression.operator.token_type == scanner.TokenType.STAR
    assert isinstance(expression.right.expression, expr.Binary)
    assert isinstance(expression.right.expression.left, expr.Literal)
    assert isinstance(expression.right.expression.right, expr.Literal)
    assert expression.right.expression.operator.token_type == scanner.TokenType.PLUS


def test_parse_assignment() -> None:
    """ """
    statements = source_to_statements(source="var a; print a;")
    assert len(statements) == 2

    var_declaration = statements[0]
    assert isinstance(var_declaration, statem.Var)
    assert var_declaration.name.token_type == scanner.TokenType.IDENTIFIER
    assert var_declaration.name.lexeme == "a"
    assert var_declaration.name.literal is None
    assert var_declaration.initializer is None

    print_statement = statements[1]
    assert isinstance(print_statement, statem.Print)
    assert isinstance(print_statement.expression, expr.Variable)
    assert print_statement.expression.name.token_type == scanner.TokenType.IDENTIFIER
    assert print_statement.expression.name.lexeme == "a"
    assert print_statement.expression.name.literal is None

    statements = source_to_statements(source="var a = 1; print a;")
    assert len(statements) == 2

    var_declaration = statements[0]
    assert isinstance(var_declaration, statem.Var)
    assert var_declaration.name.token_type == scanner.TokenType.IDENTIFIER
    assert var_declaration.name.lexeme == "a"
    assert var_declaration.name.literal is None
    assert isinstance(var_declaration.initializer, expr.Literal)
    assert var_declaration.initializer.value == 1

    print_statement = statements[1]
    assert isinstance(print_statement, statem.Print)
    assert isinstance(print_statement.expression, expr.Variable)
    assert print_statement.expression.name.token_type == scanner.TokenType.IDENTIFIER
    assert print_statement.expression.name.lexeme == "a"
    assert print_statement.expression.name.literal is None

    statements = source_to_statements(source="var a = 1; a = 2; print a + 3;")

    var_declaration = statements[0]
    assert isinstance(var_declaration, statem.Var)
    assert var_declaration.name.token_type == scanner.TokenType.IDENTIFIER
    assert var_declaration.name.lexeme == "a"
    assert var_declaration.name.literal is None
    assert isinstance(var_declaration.initializer, expr.Literal)
    assert var_declaration.initializer.value == 1

    assignment = statements[1]
    assert isinstance(assignment, statem.Expression)
    assert isinstance(assignment.expression, expr.Assign)
    assert assignment.expression.name.token_type == scanner.TokenType.IDENTIFIER
    assert assignment.expression.name.lexeme == "a"
    assert assignment.expression.name.literal is None
    assert isinstance(assignment.expression.value, expr.Literal)
    assert assignment.expression.value.value == 2

    print_statement = statements[2]
    assert isinstance(print_statement, statem.Print)
    assert isinstance(print_statement.expression, expr.Binary)
    assert isinstance(print_statement.expression.left, expr.Variable)
    assert (
        print_statement.expression.left.name.token_type == scanner.TokenType.IDENTIFIER
    )
    assert print_statement.expression.left.name.lexeme == "a"
    assert print_statement.expression.left.name.literal is None
    assert print_statement.expression.operator.token_type == scanner.TokenType.PLUS
    assert isinstance(print_statement.expression.right, expr.Literal)
    assert print_statement.expression.right.value == 3


def test_parse_scope() -> None:
    """ """
    statements = source_to_statements(
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

    var_declaration_first_a = statements[0]
    assert isinstance(var_declaration_first_a, statem.Var)
    assert var_declaration_first_a.name.token_type == scanner.TokenType.IDENTIFIER
    assert var_declaration_first_a.name.lexeme == "a"
    assert var_declaration_first_a.name.literal is None
    assert isinstance(var_declaration_first_a.initializer, expr.Literal)
    assert var_declaration_first_a.initializer.value == 1

    var_declaration_first_b = statements[1]
    assert isinstance(var_declaration_first_b, statem.Var)
    assert var_declaration_first_b.name.token_type == scanner.TokenType.IDENTIFIER
    assert var_declaration_first_b.name.lexeme == "b"
    assert var_declaration_first_b.name.literal is None
    assert isinstance(var_declaration_first_b.initializer, expr.Literal)
    assert var_declaration_first_b.initializer.value == 2

    var_declaration_first_c = statements[2]
    assert isinstance(var_declaration_first_c, statem.Var)
    assert var_declaration_first_c.name.token_type == scanner.TokenType.IDENTIFIER
    assert var_declaration_first_c.name.lexeme == "c"
    assert var_declaration_first_c.name.literal is None
    assert isinstance(var_declaration_first_c.initializer, expr.Literal)
    assert var_declaration_first_c.initializer.value == 3

    block_first = statements[3]
    assert isinstance(block_first, statem.Block)

    var_declaration_second_a = block_first.statements[0]
    assert isinstance(var_declaration_second_a, statem.Var)
    assert var_declaration_second_a.name.token_type == scanner.TokenType.IDENTIFIER
    assert var_declaration_second_a.name.lexeme == "a"
    assert var_declaration_second_a.name.literal is None
    assert isinstance(var_declaration_second_a.initializer, expr.Literal)
    assert var_declaration_second_a.initializer.value == 10

    var_declaration_second_b = block_first.statements[1]
    assert isinstance(var_declaration_second_b, statem.Var)
    assert var_declaration_second_b.name.token_type == scanner.TokenType.IDENTIFIER
    assert var_declaration_second_b.name.lexeme == "b"
    assert var_declaration_second_b.name.literal is None
    assert isinstance(var_declaration_second_b.initializer, expr.Literal)
    assert var_declaration_second_b.initializer.value == 20

    block_second = block_first.statements[2]
    assert isinstance(block_second, statem.Block)

    var_declaration_third_a = block_second.statements[0]
    assert isinstance(var_declaration_third_a, statem.Var)
    assert var_declaration_third_a.name.token_type == scanner.TokenType.IDENTIFIER
    assert var_declaration_third_a.name.lexeme == "a"
    assert var_declaration_third_a.name.literal is None
    assert isinstance(var_declaration_third_a.initializer, expr.Literal)
    assert var_declaration_third_a.initializer.value == 100

    print_statement_first_a = block_second.statements[1]
    assert isinstance(print_statement_first_a, statem.Print)
    assert isinstance(print_statement_first_a.expression, expr.Variable)
    assert (
        print_statement_first_a.expression.name.token_type
        == scanner.TokenType.IDENTIFIER
    )
    assert print_statement_first_a.expression.name.lexeme == "a"
    assert print_statement_first_a.expression.name.literal is None

    print_statement_first_b = block_second.statements[2]
    assert isinstance(print_statement_first_b, statem.Print)
    assert isinstance(print_statement_first_b.expression, expr.Variable)
    assert (
        print_statement_first_b.expression.name.token_type
        == scanner.TokenType.IDENTIFIER
    )
    assert print_statement_first_b.expression.name.lexeme == "b"
    assert print_statement_first_b.expression.name.literal is None

    print_statement_first_c = block_second.statements[3]
    assert isinstance(print_statement_first_c, statem.Print)
    assert isinstance(print_statement_first_c.expression, expr.Variable)
    assert (
        print_statement_first_c.expression.name.token_type
        == scanner.TokenType.IDENTIFIER
    )
    assert print_statement_first_c.expression.name.lexeme == "c"
    assert print_statement_first_c.expression.name.literal is None

    print_statement_second_a = block_first.statements[3]
    assert isinstance(print_statement_second_a, statem.Print)
    assert isinstance(print_statement_second_a.expression, expr.Variable)
    assert (
        print_statement_second_a.expression.name.token_type
        == scanner.TokenType.IDENTIFIER
    )
    assert print_statement_second_a.expression.name.lexeme == "a"
    assert print_statement_second_a.expression.name.literal is None

    print_statement_second_b = block_first.statements[4]
    assert isinstance(print_statement_second_b, statem.Print)
    assert isinstance(print_statement_second_b.expression, expr.Variable)
    assert (
        print_statement_second_b.expression.name.token_type
        == scanner.TokenType.IDENTIFIER
    )
    assert print_statement_second_b.expression.name.lexeme == "b"
    assert print_statement_second_b.expression.name.literal is None

    print_statement_second_c = block_first.statements[5]
    assert isinstance(print_statement_second_c, statem.Print)
    assert isinstance(print_statement_second_c.expression, expr.Variable)
    assert (
        print_statement_second_c.expression.name.token_type
        == scanner.TokenType.IDENTIFIER
    )
    assert print_statement_second_c.expression.name.lexeme == "c"
    assert print_statement_second_c.expression.name.literal is None

    print_statement_third_a = statements[4]
    assert isinstance(print_statement_third_a, statem.Print)
    assert isinstance(print_statement_third_a.expression, expr.Variable)
    assert (
        print_statement_third_a.expression.name.token_type
        == scanner.TokenType.IDENTIFIER
    )
    assert print_statement_third_a.expression.name.lexeme == "a"
    assert print_statement_third_a.expression.name.literal is None

    print_statement_third_b = statements[5]
    assert isinstance(print_statement_third_b, statem.Print)
    assert isinstance(print_statement_third_b.expression, expr.Variable)
    assert (
        print_statement_third_b.expression.name.token_type
        == scanner.TokenType.IDENTIFIER
    )
    assert print_statement_third_b.expression.name.lexeme == "b"
    assert print_statement_third_b.expression.name.literal is None

    print_statement_third_c = statements[6]
    assert isinstance(print_statement_third_c, statem.Print)
    assert isinstance(print_statement_third_c.expression, expr.Variable)
    assert (
        print_statement_third_c.expression.name.token_type
        == scanner.TokenType.IDENTIFIER
    )
    assert print_statement_third_c.expression.name.lexeme == "c"
    assert print_statement_third_c.expression.name.literal is None
