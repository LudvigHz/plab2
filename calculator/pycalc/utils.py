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
        self.func = func

    def execute(self, element, debug=False):
        if not isinstance(element, numbers.Number):
            raise TypeError("Cannot execute function on a non number element")
        result = self.func(element)
        if debug:
            print(f"Function: {self.func.__name__} ({element}) = {result}")
        return result
