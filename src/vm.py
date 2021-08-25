from typing import List, Tuple, Optional
import dataclasses

import compiler


STACK_MAX = 8


@dataclasses.dataclass
class VM:
    """ """

    bytecode: List[compiler.Byte]
    ip: int
    stack: List[Optional[int]]
    top: int


def init_vm(bytecode: List[compiler.Byte]) -> VM:
    """ """
    stack: List[Optional[int]] = [None] * STACK_MAX
    return VM(bytecode=bytecode, ip=0, stack=stack, top=0)


def push(emulator: VM, value: int) -> VM:
    """ """
    emulator.stack[emulator.top] = value
    emulator.top += 1

    return emulator


def pop(emulator: VM) -> Tuple[VM, int]:
    """ """
    emulator.top -= 1
    value = emulator.stack[emulator.top]

    assert value is not None
    return emulator, value


def read_byte(emulator: VM) -> Tuple[VM, compiler.Byte]:
    """ """
    emulator.ip += 1
    instruction = emulator.bytecode[emulator.ip - 1]

    return emulator, instruction


def read_constant(emulator: VM) -> Tuple[VM, int]:
    """ """
    emulator, constant = read_byte(emulator)

    assert isinstance(constant, int)
    return emulator, constant


def binary_op(emulator: VM, op: str) -> VM:
    """ """
    emulator, b = pop(emulator)
    emulator, a = pop(emulator)

    return push(emulator, eval(f"a {op} b"))


def is_at_end(emulator: VM) -> bool:
    """ """
    return emulator.ip == len(emulator.bytecode)


def run(emulator: VM) -> int:
    """ """
    while True:
        if is_at_end(emulator):
            break

        emulator, instruction = read_byte(emulator)

        if instruction == compiler.OpCode.OP_CONSTANT:
            emulator, constant = read_constant(emulator)
            emulator = push(emulator, constant)

        elif instruction == compiler.OpCode.OP_ADD:
            emulator = binary_op(emulator, "+")

        elif instruction == compiler.OpCode.OP_MULTIPLY:
            emulator = binary_op(emulator, "*")

    _, value = pop(emulator)
    return value
