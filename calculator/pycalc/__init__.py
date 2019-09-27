import numbers

import numpy as np

from .utils import *


class Calculator:
    def __init__(self, functions={}, operations={}, **kwargs):
        self.functions = {
            "EXP": Function(np.exp),
            "LOG": Function(np.log),
            "SIN": Function(np.sin),
            "COS": Function(np.cos),
            "SQRT": Function(np.sqrt),
        }

        self.operators = {
            "ADD": Operator(np.add, strength=0),
            "MULT": Operator(np.multiply, strength=1),
            "DIV": Operator(np.divide, strength=1),
            "SUB": Operator(np.subtract, strength=1),
        }

        self.functions.update(functions)
        self.operators.update(operations)

        self.output_queue = Queue()

    @property
    def supported_operations(self):
        return list(self.operators.keys())

    @property
    def supported_functions(self):
        return list(self.functions.keys())

    def execute_rpn(self, calculation):
        """
        Method to execute a calculation in the form of
        reverse polish notation.
        :param calculation: Queue. Should contain numbers, operations, functions
        :return int, float
        """
        value_stack = Stack()
        while not calculation.is_empty:
            # apply operations until the stack is rmpty
            el = calculation.pop()
            if isinstance(el, numbers.Number):
                value_stack.push(el)
            elif isinstance(el, Function):
                res = el.execute(value_stack.pop())
                value_stack.push(res)
            elif isinstance(el, Operator):
                res = el.execute(value_stack.pop(), value_stack.pop())
                value_stack.push(res)
        # return when we are done calculating
        return value_stack.pop()

    def execute_string(self, calculation):
        """
        Method to execute a calculation in the form of a string
        :param calculation: string. Should contain numbers, operations, functions
        :return int, float
        """
