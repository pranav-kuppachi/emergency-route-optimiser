class _Node:
    def __init__(self,priority,item):
        self.priority=priority
        self.item=item
        self.degree=0
        self.parent=None
        self.child=None
        self.sibling=None


def _link_trees(tree1, tree2):
    if tree2.priority < tree1.priority:
        tree1, tree2 = tree2, tree1

    tree2.parent = tree1
    tree2.sibling = tree1.child
    tree1.child = tree2
    tree1.degree += 1

    return tree1



def _merge_root_lists(head1, head2):
    dummy = _Node(0, None)
    tail = dummy

    while head1 is not None and head2 is not None:
        if head1.degree <= head2.degree:
            tail.sibling = head1
            head1 = head1.sibling
        else:
            tail.sibling = head2
            head2 = head2.sibling

        tail = tail.sibling

    if head1 is not None:
        tail.sibling = head1
    else:
        tail.sibling = head2

    return dummy.sibling

def _consolidate(head):
    previous=None
    current=head

    while current is not None and current.sibling is not None:
        next_root=current.sibling

        if current.degree != next_root.degree:
            previous = current
            current = next_root
            continue

        if (next_root.sibling is not None and next_root.degree == next_root.sibling.degree):
            previous = current
            current = next_root
            continue

        if current.priority <= next_root.priority:
            current.sibling = next_root.sibling
            _link_trees(current, next_root)

        else:
            if previous is None:
                head = next_root
            else:
                previous.sibling = next_root

            _link_trees(next_root, current)
            current = next_root
    return head

def _union_root_lists(head1, head2):
    merged_head = _merge_root_lists(head1, head2)
    return _consolidate(merged_head)

def _reverse_children(node):
    previous=None
    current=node.child
    while current is not None:
        next_node=current.sibling
        current.parent=None
        current.sibling=previous
        previous=current
        current=next_node
    return previous

class BinomialHeap:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, priority, item):
        new_node = _Node(priority, item)
        self.head = _union_root_lists(self.head, new_node)

    def pop_min(self):
        if self.head is None:
            raise IndexError
        min_root=self.head
        min_previous=None
        current=self.head
        previous=None
        while current is not None:
            if(current.priority<min_root.priority):
                min_root=current
                min_previous=previous
            previous = current
            current = current.sibling
        if min_previous is None:
            self.head = min_root.sibling
        else:
            min_previous.sibling = min_root.sibling
        min_root.sibling = None
        child_head = _reverse_children(min_root)
        self.head = _union_root_lists(self.head, child_head)

        return min_root.priority, min_root.item
