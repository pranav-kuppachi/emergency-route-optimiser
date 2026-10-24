class _Node:
    def __init__(self, priority, item):
        self.priority = priority
        self.item = item
        self.left = None
        self.right = None
        self.npl = 0


class LeftistHeap:
    def __init__(self):
        self.root = None
    def _get_npl(self, node):
        if node is None:
            return -1
        return node.npl
    def _merge(self, h1, h2):
        if h1 is None:
            return h2

        if h2 is None:
            return h1

        if h1.priority > h2.priority:
            h1, h2 = h2, h1

        h1.right = self._merge(h1.right, h2)

        if self._get_npl(h1.left) < self._get_npl(h1.right):
            h1.left, h1.right = h1.right, h1.left

        h1.npl = 1 + min(
            self._get_npl(h1.left),
            self._get_npl(h1.right)
        )

        return h1
    def push(self, priority, item):
        if not isinstance(priority, int) or isinstance(priority, bool):
            raise TypeError("priority must be an integer")

        if priority < 0:
            raise ValueError("priority cannot be negative")

        new_node = _Node(priority, item)
        self.root = self._merge(self.root, new_node)
    def pop_min(self):
        if self.root is None:
            raise IndexError("pop_min from an empty heap")

        priority = self.root.priority
        item = self.root.item

        self.root = self._merge(self.root.left, self.root.right)

        return priority, item
    def is_empty(self):
        return self.root is None
