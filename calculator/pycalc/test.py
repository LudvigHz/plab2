import math
import unittest

import numpy as np

from pycalc import Calculator, Function, Operator, Queue, Stack


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()
        self.queue.push(1)
        self.queue.push(2)
        self.queue.push(3)
        self.queue.push(4)
        self.queue.push(5)

    def test_create_queue_and_add_item(self):
        queue = Queue()
        self.assertTrue(queue.is_empty)
        queue.push(1)
        self.assertFalse(queue.is_empty)
        self.assertEqual(queue.size, 1)
        self.assertEqual(queue.peek(), 1)

    def test_len_and_peek(self):
        self.assertEqual(self.queue.size, 5)
        self.assertEqual(self.queue.peek(), 1)

    def test_pop(self):
        queue = Queue()
        queue.push(1)
        queue.push(2)
        queue.push(3)
        self.assertEqual(queue.pop(), 1)
        self.assertEqual(queue.peek(), 2)
        self.assertEqual(queue.size, 2)


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.stack.push(4)
        self.stack.push(5)

    def test_create_stack_and_add_item(self):
        stack = Stack()
        self.assertTrue(stack.is_empty)
        stack.push(1)
        self.assertFalse(stack.is_empty)
        self.assertEqual(stack.size, 1)
        self.assertEqual(stack.peek(), 1)

    def test_len_and_peek(self):
        self.assertEqual(self.stack.size, 5)
        self.assertEqual(self.stack.peek(), 5)

    def test_pop(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.peek(), 2)
        self.assertEqual(stack.size, 2)


class TestFunctionAndOperator(unittest.TestCase):
    def setUp(self):
        self.sin_function = Function(math.sin)
        self.floor_function = Function(math.floor)
        self.add_operator = Operator(np.add)
        self.modulo_operator = Operator(np.mod)

    def test_create_function_illegal_arguments(self):
        """A function needs a function as an argument"""
        self.assertRaises(TypeError, Function, "a")
        self.assertRaises(TypeError, Function, 1)

    def test_function_execute(self):
        """A function should execute and return the correct value"""
        self.assertEqual(self.sin_function.execute(4), math.sin(4))
        self.assertEqual(self.floor_function.execute(2.89), math.floor(2.89))

    def test_operator_illegal_argument(self):
        """An operator needs a function as an argument"""
        self.assertRaises(TypeError, Operator, "a")
        self.assertRaises(TypeError, Operator, 1)

    def test_operator_execute(self):
        """An operator should give the correct result"""
        self.assertEqual(self.add_operator.execute(1, 3), 1 + 3)
        self.assertEqual(self.modulo_operator.execute(5, 2), 5 % 2)


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.defaultCalc = Calculator()
        self.defaultOperations = self.defaultCalc.supported_operations
        self.defaultFunctions = self.defaultCalc.supported_functions

    def test_create_calculator(self):
        """
        A calculator should be created with no or all options
        """
        ops = {"MOD": np.mod, "ABS": np.abs}
        funcs = {"TAN": np.tan}

        calcWithOperations = Calculator(operations=ops)
        self.assertEqual(
            calcWithOperations.supported_operations,
            self.defaultOperations + list(ops.keys()),
        )

        calcWithFunctions = Calculator(functions=funcs)
        self.assertEqual(
            calcWithFunctions.supported_functions,
            self.defaultFunctions + list(funcs.keys()),
        )

    def test_calculator_execute(self):
        """A calculator should give the correct results"""
        self.assertEqual(self.defaultCalc.operators["MULT"].execute(2, 3), 2 * 3)
        self.assertEqual(self.defaultCalc.operators["ADD"].execute(2, 3), 2 + 3)
        self.assertEqual(self.defaultCalc.functions["EXP"].execute(2), np.exp(2))
        self.assertEqual(self.defaultCalc.functions["SIN"].execute(2), np.sin(2))
        self.assertEqual(
            self.defaultCalc.functions["EXP"].execute(
                self.defaultCalc.operators["ADD"].execute(
                    1, self.defaultCalc.operators["MULT"].execute(2, 3)
                )
            ),
            np.exp(1 + 2 * 3),
        )

    def test_rpn_calculation(self):
        """A calculator executing a rpn calculation should give the corrrect result"""
        calculation = Queue()
        calculation.push(1)
        calculation.push(2)
        calculation.push(3)
        calculation.push(self.defaultCalc.operators["MULT"])
        calculation.push(self.defaultCalc.operators["ADD"])
        calculation.push(self.defaultCalc.functions["EXP"])
        self.assertEqual(self.defaultCalc.execute_rpn(calculation), np.exp(1 + 2 * 3))

    def test_convert_to_rpn(self):
        """
        A calculator should successfully convert
        from a stack containing the calculation to RPN
        """
        calculation = Queue()
        calculation.push(self.defaultCalc.functions["EXP"])
        calculation.push("(")
        calculation.push(1.0)
        calculation.push(self.defaultCalc.operators["ADD"])
        calculation.push(2.0)
        calculation.push(self.defaultCalc.operators["MULT"])
        calculation.push(3.0)
        calculation.push(")")
        calculation.push(self.defaultCalc.operators["SUB"])
        calculation.push(1.0)

        rpn_queue = Queue()
        rpn_queue.push(1.0)
        rpn_queue.push(2.0)
        rpn_queue.push(3.0)
        rpn_queue.push(self.defaultCalc.operators["MULT"])
        rpn_queue.push(self.defaultCalc.operators["ADD"])
        rpn_queue.push(self.defaultCalc.functions["EXP"])
        rpn_queue.push(1.0)
        rpn_queue.push(self.defaultCalc.operators["SUB"])

        self.assertEqual(self.defaultCalc.to_rpn(calculation)._items, rpn_queue._items)
        calculation.push("SUB")

    def test_parse_string_to_calculation(self):
        """
        A calculator should successfully convert
        from a stack containing the calculation to RPN
        """
        calculation = Queue()
        calculation.push(self.defaultCalc.functions["EXP"])
        calculation.push("(")
        calculation.push(1.0)
        calculation.push(self.defaultCalc.operators["ADD"])
        calculation.push(2.0)
        calculation.push(self.defaultCalc.operators["MULT"])
        calculation.push(3.0)
        calculation.push(")")
        calculation.push(self.defaultCalc.operators["SUB"])
        calculation.push(1.0)

        self.assertEqual(
            self.defaultCalc.parse_string("exp(1 add 2 mult 3) sub 1")._items,
            calculation._items,
        )

    def test_calculation_from_string(self):
        """
        A calculator should give the correct results when given a string with
        a calculation.
        """
        self.assertEqual(
            self.defaultCalc.calculate_expression("exp(1 add 2 mult 3) sub 1"),
            np.exp(1 + 2 * 3) - 1,
        )

        self.assertEqual(
            self.defaultCalc.calculate_expression("sqrt(3) mult 2 sub 9 div 2"),
            np.sqrt(3) * 2 - 9 / 2,
        )

        self.assertEqual(
            self.defaultCalc.calculate_expression(
                "((15 div (7 sub (1 add 1))) mult 3) sub (2 add (1 add 1))"
            ),
            ((15 / (7 - (1 + 1))) * 3) - (2 + (1 + 1)),
        )
