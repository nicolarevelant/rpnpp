#!/usr/bin/env python3

import math
import os
import sys

DEBUG = False
if os.environ.get("RPNPP_DEBUG") == "1":
    DEBUG = True
elif "-d" in sys.argv:
    DEBUG = True

# Notazione polacca inversa con assegnazione variabili

OPERATIONS = {
        # arithmetic
        "+": [lambda x, y : x + y, float, float],
        "-": [lambda x, y : x - y, float, float],
        "*": [lambda x, y : x * y, float, float],
        "/": [lambda x, y : x / y, float, float],
        "**": [lambda x, y : x ** y, float, float],
        "sin": [lambda x : math.sin(x), float],
        "cos": [lambda x : math.cos(x), float],
        "tan": [lambda x : math.tan(x), float],

        # logical
        "<": [lambda x, y: x < y, float, float],
        ">": [lambda x, y: x > y, float, float],
        "<=": [lambda x, y: x <= y, float, float],
        ">=": [lambda x, y: x >= y, float, float],
        "==": [lambda x, y: x == y, float, float],

        # condition
        "if": [lambda x, y, cond: x if cond else y, None, None, bool],
}


def read_row():
    try:
        value = input()
        return value
    except EOFError:
        return None

def try_float(value):
    try:
        return float(value)
    except:
        return None

def try_bool(value):
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

def handleOperation(stack, opName, op):
    # op[0]: lambda
    # len(op) - 1: # of arguments
    # op[1..len(op)-1]: arguments
    if len(stack) < len(op) - 1:
        print(f" [EE] Stack does not contain enough arguments for OP: \"{opName}\"")
        return False

    args = []
    for i in range(1, len(op)):
        arg = stack.pop()
        if op[-i] is None or type(arg) is op[-i]:
            args.insert(0, arg) # last removed item is the first argument
        else:
            isError = True
            print(f" [EE] Type mismatch: expected \"{op[i]}\" but type({arg}) == \"{type(arg)}\"")
            return False

    if DEBUG:
        print(f" [DD] Executing OP: {args} \"{opName}\"")

    result = op[0](*args)
    stack.append(result)

    return True

def handleVariables(stack, variables, value):
    if value[0] == '$':
        # variable substitution
        num = variables.get(value[1:])
        if num is None:
            print(f" [EE] Variable not found: {value}")
            return False
        stack.append(num)
    elif len(stack) > 0:
        # variable assignment
        variables[value] = stack.pop()
    else:
        print(f" [EE] Empty stack while trying to fetch an item to be assigned to VAR: \"{value}\"")
        return False

    return True

def main():
    isError = False
    stack = []
    variables = {}
    while not isError:
        row = read_row()
        if row is None:
            break

        for value in row.split():
            num = try_float(value)
            if num is not None:
                stack.append(num)
                continue
            num = try_bool(value)
            if num is not None:
                stack.append(num)
                continue

            op = OPERATIONS.get(value)
            if op is not None:
                # operation
                if not handleOperation(stack, value, op):
                    isError = True
                    break
            else:
                # variables
                if not handleVariables(stack, variables, value):
                    isError = True
                    break

        if DEBUG:
            print(f" [DD] Stack: {stack}")

    if len(stack) == 1:
        print(stack[0])
        return not isError

    print(stack)
    return False

if __name__ == "__main__":
    if not main():
        exit(1)
