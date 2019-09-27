import unittest
from pycalc import Queue, Stack


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
