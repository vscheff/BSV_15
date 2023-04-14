# Computes the index of the parent node for a given index
def get_parent(i: int) -> int:
    return (i - 1) // 2


# Computes the index of the node to the left of a given index
def get_left(i: int) -> int:
    return 2 * i + 1


# Computes the index of the node to the right of a given index
def get_right(i) -> int:
    return 2 * i + 2


# Implementation of a Min Heap data structure
# attr nodes - underlying array that holds each node in the heap
class MinHeap:
    def __init__(self):
        self.nodes = []

    def __len__(self) -> int:
        return len(self.nodes)

    def __bool__(self) -> bool:
        return bool(self.nodes)

    # Swaps the nodes at two given indexes
    # param a - first index
    # param b - second index
    def swap(self, a, b):
        self.nodes[a], self.nodes[b] = self.nodes[b], self.nodes[a]

    # Recursive function that ensures the order property of our min heap
    # param index - index of the element that is potentially in the wrong place
    def heapify(self, index: int):
        left = get_left(index)
        right = get_right(index)
        smallest = index

        # Determine which of the three nodes has the smallest frequency
        if left < len(self.nodes) and self.nodes[left] < self.nodes[smallest]:
            smallest = left
        if right < len(self.nodes) and self.nodes[right] < self.nodes[smallest]:
            smallest = right

        # Swap node at index with the smallest node, and make a recursive call
        if smallest != index:
            self.swap(index, smallest)
            self.heapify(smallest)

    # Inserts a node into the min heap
    # param new_node - the node to be inserted
    def insert(self, new_node):
        i = len(self.nodes)
        j = get_parent(i)
        self.nodes.append(new_node)

        # Move the new node up the tree ensuring the heap satisfies the order property
        while i and self.nodes[i] < self.nodes[j]:
            self.swap(i, j)
            i = j
            j = get_parent(i)

    # Removes and returns the root node of the heap
    # return      None - if the heap is empty
    # return root_node - node at the root of the tree
    def pop_root(self):
        if not self.nodes:
            print("ERROR: Heap Empty! Nothing to pop.\n")
            return None

        if len(self.nodes) == 1:
            return self.nodes.pop(0)

        root_node = self.nodes.pop(0)
        self.nodes.insert(0, self.nodes.pop())
        self.heapify(0)

        return root_node

    # Clears the heap
    def clear(self):
        self.nodes.clear()
