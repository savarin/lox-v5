from typing import List, Tuple, Optional
import dataclasses

import compiler


STACK_MAX = 8


@dataclasses.dataclass
class VM:
    """ """

    bytecode: List[compiler.Byte]
    values: compiler.Values
    ip: int
    stack: List[Optional[int]]
    stack_top: int


def init_vm(bytecode: List[compiler.Byte], values: compiler.Values) -> VM:
    """ """
    stack: List[Optional[int]] = [None] * STACK_MAX
    return VM(bytecode=bytecode, values=values, ip=0, stack=stack, stack_top=0)


def run(hypervisor: VM) -> List[str]:
    """ """
    result: List[str] = []

    while not is_at_end(hypervisor):
        hypervisor, instruction = read_byte(hypervisor)

        if instruction == compiler.OpCode.OP_CONSTANT:
            hypervisor, constant = read_constant(hypervisor)
            hypervisor = push(hypervisor, constant)

        elif instruction == compiler.OpCode.OP_POP:
            hypervisor, value = pop(hypervisor)

        elif instruction == compiler.OpCode.OP_GET:
            hypervisor, location = read_byte(hypervisor)

            assert isinstance(location, int)
            value = hypervisor.stack[location]
            hypervisor = push(hypervisor, value)

        elif instruction == compiler.OpCode.OP_SET:
            hypervisor, location = read_byte(hypervisor)
            value = hypervisor.stack[hypervisor.stack_top - 1]

            assert isinstance(location, int)
            hypervisor.stack[location] = value

        elif instruction == compiler.OpCode.OP_ADD:
            hypervisor = binary_op(hypervisor, "+")

        elif instruction == compiler.OpCode.OP_SUBTRACT:
            hypervisor = binary_op(hypervisor, "-")

        elif instruction == compiler.OpCode.OP_MULTIPLY:
            hypervisor = binary_op(hypervisor, "*")

        elif instruction == compiler.OpCode.OP_PRINT:
            hypervisor, value = pop(hypervisor)
            result.append(str(value or "nil"))

    return result


def push(hypervisor: VM, constant: Optional[int]) -> VM:
    """ """
    hypervisor.stack[hypervisor.stack_top] = constant
    hypervisor.stack_top += 1

    return hypervisor


def pop(hypervisor: VM) -> Tuple[VM, Optional[int]]:
    """ """
    hypervisor.stack_top -= 1
    item = hypervisor.stack[hypervisor.stack_top]

    # assert item is not None
    return hypervisor, item


def read_byte(hypervisor: VM) -> Tuple[VM, compiler.Byte]:
    """ """
    hypervisor.ip += 1
    instruction = hypervisor.bytecode[hypervisor.ip - 1]

    return hypervisor, instruction


def read_constant(hypervisor: VM) -> Tuple[VM, Optional[int]]:
    """ """
    hypervisor, location = read_byte(hypervisor)

    if location is None:
        return hypervisor, None

    assert isinstance(location, int)
    return hypervisor, hypervisor.values.array[location]


def binary_op(hypervisor: VM, op: str) -> VM:
    """ """
    hypervisor, b = pop(hypervisor)
    hypervisor, a = pop(hypervisor)

    return push(hypervisor, eval(f"a {op} b"))


def is_at_end(hypervisor: VM) -> bool:
    """ """
    return hypervisor.ip == len(hypervisor.bytecode)
