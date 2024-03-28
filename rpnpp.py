#!/usr/bin/env python3

import math

# Notazione polacca inversa con assegnazione variabili

OPERATIONS = {
        "+": [2, lambda x, y : x + y],
        "-": [2, lambda x, y : x - y],
        "*": [2, lambda x, y : x * y],
        "/": [2, lambda x, y : x / y],
        "**": [2, lambda x, y : x ** y],
        "sin": [1, lambda x : math.sin(x)],
        "cos": [1, lambda x : math.cos(x)],
        "tan": [1, lambda x : math.tan(x)],
        }

variables = {}

def read_row():
    try:
        value = input()
        return value
    except EOFError:
        return None

def main():
    isError = False
    stack = []
    row = read_row()
    while not isError and row is not None:
        for value in row.split():
            # decide if value is a number or a operator
            try:
                # number
                num = float(value)
                stack.append(num)
            except ValueError:
                # not a number
                op = OPERATIONS.get(value)
                if op is None:
                    if value[0] == '$':
                        # variable substitution
                        num = variables.get(value[1:])
                        if num is None:
                            isError = True
                            print(f" [EE] Variable not found: {value}")
                        else:
                            stack.append(num)
                    elif len(stack) > 0:
                        # variable assignment
                        variables[value] = stack.pop()
                    else:
                        isError = True
                        print(f" [EE] Empty stack while trying to fetch an item to be assigned to VAR: \"{value}\"")
                else:
                    # operation
                    # [0]: 1 argument --> False, 2 arguments --> True
                    # [1]: lambda
                    args = []
                    if len(stack) >= op[0]:
                        for i in range(op[0]):
                            args.insert(0, stack.pop())
                        result = op[1](*args)
                        
                        stack.append(result)
                    else:
                        isError = True
                        print(f" [EE] Empty stack while trying to fetch arguments for OP: \"{value}\"")
        
        if not isError:
            row = read_row()

    print("------------------------------------")
    print(stack)


if __name__ == "__main__":
    main()
