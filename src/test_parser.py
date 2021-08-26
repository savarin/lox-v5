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
    statements = source_to_statements(source="print 1 * (2 + 3);")
    assert len(statements) == 1

    statement = statements[0]
    assert isinstance(statement, statem.Print)

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


def test_parse_function() -> None:
    """ """
    statements = source_to_statements(
        source="fun add(a, b) { print a + b; } add(1, 2);"
    )
    assert len(statements) == 2

    function = statements[0]
    assert isinstance(function, statem.Function)
    assert function.name.lexeme == "add"
    assert function.parameters[0].lexeme == "a"
    assert function.parameters[1].lexeme == "b"

    body = function.body[0]
    assert isinstance(body, statem.Print)
    assert isinstance(body.expression, expr.Binary)
    assert isinstance(body.expression.operator, scanner.Token)
    assert body.expression.operator.lexeme == "+"
    assert isinstance(body.expression.left, expr.Variable)
    assert body.expression.left.name.lexeme == "a"
    assert isinstance(body.expression.right, expr.Variable)
    assert body.expression.right.name.lexeme == "b"

    call = statements[1]
    assert isinstance(call, statem.Expression)
    assert isinstance(call.expression, expr.Call)
    assert isinstance(call.expression.callee, expr.Variable)
    assert call.expression.callee.name.lexeme == "add"
    assert isinstance(call.expression.arguments[0], expr.Literal)
    assert call.expression.arguments[0].value == 1
    assert isinstance(call.expression.arguments[1], expr.Literal)
    assert call.expression.arguments[1].value == 2

    statements = source_to_statements(
        source="fun count(n) { if (n == 1) return 1; return count(n - 1); } print count(3);"
    )
    assert len(statements) == 2

    function = statements[0]
    assert isinstance(function, statem.Function)
    assert function.name.lexeme == "count"
    assert function.parameters[0].lexeme == "n"

    body = function.body[0]
    assert isinstance(body, statem.If)
    assert isinstance(body.condition, expr.Binary)
    assert body.condition.operator.lexeme == "=="
    assert isinstance(body.condition.left, expr.Variable)
    assert body.condition.left.name.lexeme == "n"
    assert isinstance(body.condition.right, expr.Literal)
    assert body.condition.right.value == 1

    then_branch = body.then_branch
    assert isinstance(then_branch, statem.Return)
    assert isinstance(then_branch.keyword, scanner.Token)
    assert then_branch.keyword.lexeme == "return"
    assert isinstance(then_branch.value, expr.Literal)
    assert then_branch.value.value == 1

    else_branch = body.else_branch
    assert else_branch is None

    return_statement = function.body[1]
    assert isinstance(return_statement, statem.Return)
    assert isinstance(return_statement.value, expr.Call)
    assert isinstance(return_statement.value.callee, expr.Variable)
    assert return_statement.value.callee.name.lexeme == "count"
    assert isinstance(return_statement.value.arguments[0], expr.Binary)
    assert return_statement.value.arguments[0].operator.lexeme == "-"
    assert isinstance(return_statement.value.arguments[0].left, expr.Variable)
    assert return_statement.value.arguments[0].left.name.lexeme == "n"
    assert isinstance(return_statement.value.arguments[0].right, expr.Literal)
    assert return_statement.value.arguments[0].right.value == 1

    call = statements[1]
    assert isinstance(call, statem.Print)
    assert isinstance(call.expression, expr.Call)
    assert isinstance(call.expression.callee, expr.Variable)
    assert call.expression.callee.name.lexeme == "count"
    assert isinstance(call.expression.arguments[0], expr.Literal)
    assert call.expression.arguments[0].value == 3

    statements = source_to_statements(
        source="fun fib(n) { if (n == 1) return 1; if (n == 2) return 1; return fib(n - 2) + fib(n - 1); } print fib(8);"
    )
    assert len(statements) == 2

    function = statements[0]
    assert isinstance(function, statem.Function)
    assert function.name.lexeme == "fib"
    assert function.parameters[0].lexeme == "n"

    body = function.body[0]
    assert isinstance(body, statem.If)
    assert isinstance(body.condition, expr.Binary)
    assert body.condition.operator.lexeme == "=="
    assert isinstance(body.condition.left, expr.Variable)
    assert body.condition.left.name.lexeme == "n"
    assert isinstance(body.condition.right, expr.Literal)
    assert body.condition.right.value == 1

    then_branch = body.then_branch
    assert isinstance(then_branch, statem.Return)
    assert isinstance(then_branch.value, expr.Literal)
    assert then_branch.value.value == 1

    body = function.body[1]
    assert isinstance(body, statem.If)
    assert isinstance(body.condition, expr.Binary)
    assert body.condition.operator.lexeme == "=="
    assert isinstance(body.condition.left, expr.Variable)
    assert body.condition.left.name.lexeme == "n"
    assert isinstance(body.condition.right, expr.Literal)
    assert body.condition.right.value == 2

    then_branch = body.then_branch
    assert isinstance(then_branch, statem.Return)
    assert isinstance(then_branch.value, expr.Literal)
    assert then_branch.value.value == 1

    return_statement = function.body[2]
    assert isinstance(return_statement, statem.Return)
    assert isinstance(return_statement.value, expr.Binary)
    assert return_statement.value.operator.lexeme == "+"

    left_call = return_statement.value.left
    assert isinstance(left_call, expr.Call)
    assert isinstance(left_call.callee, expr.Variable)
    assert left_call.callee.name.lexeme == "fib"
    assert isinstance(left_call.arguments[0], expr.Binary)
    assert left_call.arguments[0].operator.lexeme == "-"
    assert isinstance(left_call.arguments[0].left, expr.Variable)
    assert left_call.arguments[0].left.name.lexeme == "n"
    assert isinstance(left_call.arguments[0].right, expr.Literal)
    assert left_call.arguments[0].right.value == 2

    right_call = return_statement.value.right
    assert isinstance(right_call, expr.Call)
    assert isinstance(right_call.callee, expr.Variable)
    assert right_call.callee.name.lexeme == "fib"
    assert isinstance(right_call.arguments[0], expr.Binary)
    assert right_call.arguments[0].operator.lexeme == "-"
    assert isinstance(right_call.arguments[0].left, expr.Variable)
    assert right_call.arguments[0].left.name.lexeme == "n"
    assert isinstance(right_call.arguments[0].right, expr.Literal)
    assert right_call.arguments[0].right.value == 1

    expression = statements[1]
    assert isinstance(expression, statem.Print)
    assert isinstance(expression.expression, expr.Call)
    assert isinstance(expression.expression.callee, expr.Variable)
    assert expression.expression.callee.name.lexeme == "fib"
    assert isinstance(expression.expression.arguments[0], expr.Literal)
    assert expression.expression.arguments[0].value == 8
