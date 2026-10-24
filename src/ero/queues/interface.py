
from typing import Protocol, TypeVar

# T represents the type of item stored in a heap.
# In our project, an item will usually be a location ID.
T = TypeVar("T")


class HeapInterface(Protocol[T]):

    """
    Common interface for all priority queues

    Every heap must support:
    1. Inserting an item with a priority.
    2. Removing the item with the minimum priority.
    3. Checking whether the heap is empty.

    Each heap implements these operations using its own
    internal data structure.
    """

    def push(self, priority: int, item: T):
        """
        Insert an item into the heap.
        """
        ...

    def pop_min(self) -> tuple[int, T]:
        """
        Remove and return an item with the minimum priority
        """
        ...

    def is_empty(self) -> bool:
        """
        Check whether the heap contains any items.
        """
        ...
