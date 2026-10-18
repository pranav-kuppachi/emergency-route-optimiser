from typing import Protocol, TypeVar

T = TypeVar("T")


class PriorityQueue(Protocol[T]):
    """Common interface for the project's minimum-priority queues."""

    def push(self, priority: int, item: T) -> None:
        """Insert an item with its priority."""
        ...

    def pop_min(self) -> tuple[int, T]:
        """Remove and return the minimum-priority (priority, item) pair."""
        ...

    def is_empty(self) -> bool:
        """Return whether the queue contains no items."""
        ...
