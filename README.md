# minimal-lox

*This project was completed as a part of Bradfield's [Compilers](https://bradfieldcs.com/courses/languages/) class.*

## Introduction

minimal-lox is a minimal implementation of [Lox](https://craftinginterpreters.com/the-lox-language.html) that supports Fibonacci number generation.

## Context

The Lox language was introduced in [Crafting Interpreters](https://craftinginterpreters.com/contents.html), implemented first with a tree-walk interpreter (source code → tokens → AST → execution) written in Java, and second with a compiler and bytecode VM (source code → tokens → bytecode → execution) in C.

In an exercise similar to Lindsey Kuper's [post](http://composition.al/blog/2017/07/31/my-first-fifteen-compilers/), we implement Lox in Python through multiple iterations:

* [v1](https://github.com/savarin/lox-v1) - compiler; up to conditionals.
* [v2](https://github.com/savarin/lox-v2) - compiler; up to functions, with more guardrails and written in a functional style.
* [v3](https://github.com/savarin/lox-v3) - interpreter; up to scope.
* [v4](https://github.com/savarin/lox-v4) - interpreter + compiler; up to functions.
* [v5](https://github.com/savarin/minimal-lox) - interpreter + compiler; up to functions, simplified implementation.

The v4 implementation was completed as a part of Bradfield's Compiler class. The interpreter plus compiler design implements (1) source code → tokens → AST → execution, as well as (2) source code → tokens → AST → bytecode → execution. In particular, the implementation supports Fibonacci number generation as a [use case](https://github.com/savarin/lox-v4/blob/7722bc09250e6c672ab9a20ff590ac4cba1661ef/src/test_interpreter.py#L105-L110), and can be run as a REPL (example [here](https://replit.com/@savarin/lox?v=1), sample source code [here](https://gist.github.com/savarin/4ddb8de89650e92c1c723dd06bc86485)).

The v5 implementation / minimal-lox is a simplified version of v4, introduced to consolidate learning. More specifically, minimal-lox implements arithmetic operations, statements, variables, conditionals and functions.

## Components

* [expr](https://github.com/savarin/minimal-lox/blob/main/src/expr.py) - abstract class for expressions
* [statem](https://github.com/savarin/minimal-lox/blob/main/src/statem.py) - abstract class for statements
* [scanner](https://github.com/savarin/minimal-lox/blob/main/src/scanner.py) - converts raw source code into tokens
* [parser](https://github.com/savarin/minimal-lox/blob/main/src/parser.py) - converts tokens into AST via recursive descent
* [interpreter](https://github.com/savarin/minimal-lox/blob/main/src/interpreter.py) - execution by walking through the AST
* [compiler](https://github.com/savarin/minimal-lox/blob/main/src/compiler.py) - converts AST into bytecode
* [vm](https://github.com/savarin/minimal-lox/blob/main/src/vm.py) - execution by interpreting the bytecode
