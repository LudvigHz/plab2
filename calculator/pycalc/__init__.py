import numbers
import re

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
            "SUB": Operator(np.subtract, strength=0),
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
                el1 = value_stack.pop()
                el2 = value_stack.pop()
                res = el.execute(el2, el1)
                value_stack.push(res)
        # return when we are done calculating
        return value_stack.pop()

    def to_rpn(self, input_queue):
        output = Queue()
        operators = Stack()
        while not input_queue.is_empty:
            item = input_queue.pop()
            if isinstance(item, float):
                output.push(item)
            elif isinstance(item, Function):
                operators.push(item)
            elif item == "(":
                operators.push(item)
            elif item == ")":
                while operators.peek() != "(":
                    output.push(operators.pop())
                operators.pop()
            elif isinstance(item, Operator):
                while not operators.is_empty and (
                    isinstance(operators.peek(), Operator)
                    and operators.peek().strength > item.strength
                    or isinstance(operators.peek(), Function)
                ):
                    output.push(operators.pop())
                operators.push(item)
        while not operators.is_empty:
            output.push(operators.pop())

        return output

    def parse_string(self, string):
        """
        Parses a string containing a calculation to a queue.
        """
        text = string.replace(" ", "").upper()
        result = Queue()

        function_regex = r"|".join(self.supported_functions)
        operation_regex = r"|".join(self.supported_operations)
        number_regex = r"-?\d+\.?\d*"
        parenthes_start_regex = r"\("
        parenthes_end_regex = r"\)"

        matches = re.findall(
            r"("
            + ")|(".join(
                [
                    number_regex,
                    operation_regex,
                    function_regex,
                    parenthes_start_regex,
                    parenthes_end_regex,
                ]
            )
            + ")",
            text,
        )

        for match in matches:
            group = [i for i, item in enumerate(match) if item != ""][0]
            item = match[group]
            if group == 0:
                result.push(float(item))
            elif group == 1:
                result.push(self.operators[item])
            elif group == 2:
                result.push(self.functions[item])
            else:
                result.push(item)

        return result

    def calculate_expression(self, calculation):
        """
        Method to execute a calculation in the form of a string
        :param calculation: string. Should contain numbers, operations, functions
        :return int, float
        """
        parsed = self.parse_string(calculation)

        return self.execute_rpn(self.to_rpn(parsed))
