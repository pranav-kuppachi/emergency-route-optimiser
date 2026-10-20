class _Node:
    def __init__(self, priority, item):
        self.priority = priority
        self.item = item
        self.left = None
        self.right = None


class SkewHeap:
    def __init__(self):
        self.root = None

    def _merge(self, first, second):
        if first is None:
            return second
        if second is None:
            return first

        if second.priority < first.priority:
            first, second = second, first

        first.right = self._merge(first.right, second)
        first.left, first.right = first.right, first.left

        return first

    def push(self, priority, item):
        new_node = _Node(priority, item)
        self.root = self._merge(self.root, new_node)

    def pop_min(self):
        if self.root is None:
            raise IndexError("pop from an empty skew heap")

        result = (self.root.priority, self.root.item)
        self.root = self._merge(self.root.left, self.root.right)
        return result

    def is_empty(self):
        return self.root is None
