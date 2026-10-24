# Radix Heap implementation

# Priorities must be non negative integers and new entries
# cannot be smaller than the last priority removed from the heap

class RadixHeap:
    def __init__(self):
        self.last = 0  # Last priority removed from the heap
        self.size = 0  # Total number of items in the heap
        self.buckets = [[]]  # Buckets are added when needed

    def _bucket_index(self, priority):
        #  entry must be an integer 
        if type(priority) != int:
            raise TypeError("Priority must be an integer")

        # entry must be non negative 
        if priority < 0:
            raise ValueError("Priority must be non-negative")

        # XOR finds the bits that differ from the last removed priority.
        # The number of bits needed gives us the bucket index.
        return (priority ^ self.last).bit_length()

    def push(self, priority, item):
        if type(priority) != int:
            raise TypeError("Priority must be an integer")

        if priority < 0:
            raise ValueError("Priority must be non-negative")

        # New priorities cannot be smaller than the last popped priority
        if priority < self.last:
            raise ValueError("Priority cannot be smaller than last extracted priority")

        bucket = self._bucket_index(priority)

        # Creating more buckets if this priority needs one
        while bucket >= len(self.buckets):
            self.buckets.append([])

        self.buckets[bucket].append((priority, item))
        self.size += 1

    def pop_min(self):
        if self.is_empty():
            raise IndexError("pop_min from an empty RadixHeap")

        # If bucket 0 is empty, we need to redistribute another bucket
        if not self.buckets[0]:
            bucket = next(
                i for i in range(1, len(self.buckets))
                if self.buckets[i]
            )
            self._redistribute(bucket)

        # Bucket 0 contains items with entry equal to last
        priority, item = self.buckets[0].pop()
        self.size -= 1

        return priority, item

    def _redistribute(self, bucket):
        # Take all items out of this bucket before placing them again
        items = self.buckets[bucket]
        self.buckets[bucket] = []

        # The smallest priority in this bucket becomes the new last
        self.last = min(priority for priority, item in items)

        # Recalculate bucket positions using the updated last value
        for priority, item in items:
            new_bucket = self._bucket_index(priority)

            while new_bucket >= len(self.buckets):
                self.buckets.append([])

            self.buckets[new_bucket].append((priority, item))

        # size stays the same because no items were added or removed

    def is_empty(self):
        return self.size == 0
