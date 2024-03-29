import numbers


class Container:
    """
    Container superclass.
    """

    def __init__(self):
        self._items = []

    @property
    def size(self):
        return len(self._items)

    @property
    def is_empty(self):
        return len(self._items) == 0

    def push(self, item):
        self._items.append(item)

    def pop(self):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError

    def __str__(self):
        return [str(item) for item in self._items]


class Queue(Container):
    """
    A container that pushes to the end, and pops at the start
    """

    def pop(self):
        assert not self.is_empty
        return self._items.pop(0)

    def peek(self):
        assert not self.is_empty
        return self._items[0]


class Stack(Container):
    """
    A container that pushes to the end, and pops at the end
    """

    def pop(self):
        assert not self.is_empty
        return self._items.pop(-1)

    def peek(self):
        assert not self.is_empty
        return self._items[-1]


class Function:
    """
    Wrapper class for a fuction
    """

    def __init__(self, func):
        if not callable(func):
            raise TypeError("Paramenter func needs to be a function")
        self.func = func

    def execute(self, element, debug=False):
        if not isinstance(element, numbers.Number):
            raise TypeError("Cannot execute function on a non number element")
        result = self.func(element)
        if debug:
            print(f"Function: {self.func.__name__} ({element}) = {result}")
        return result

    def __str__(self):
        return self.func.__name__


class Operator:
    """
    A class for an operator used un the calculator
    """

    def __init__(self, operation, **kwargs):
        if not callable(operation):
            raise TypeError("Paramenter func needs to be a function")
        self.operation = operation
        self.strength = kwargs.get("strength", 0)

    def execute(self, a, b):
        return self.operation(a, b)

    def __str__(self):
        return self.operation.__name__
