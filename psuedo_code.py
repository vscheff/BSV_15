from minheap import MinHeap

class Puzzle:
    def is_solution(self):
        return True if solved else False

    def is_solvable(self):
        return True if possible to solve else False

    def generate(self):
        generate random puzzle

    def move(self, direction):
        move blank spot in direction

    def inv_count(self):
        return number of inversions

    def find_blank(self):
        return position of blank space

class Node:
    def cost(self):
        return depth_in_tree + number_of_inversions

puzzle = Puzzle()
while not puzzle.is_solvable():
    puzzle.generate()

liveNodes = MinHeap()
start_node = Node(puzzle.board)
liveNodes.insert(Node(puzzle.board))
current = puzzle.board

while not (current.is_solution() or liveNodes.empty()):
    current = liveNodes.pop_root()

    # Try to swap empty space in each direction
    # Add the new board to liveNodes if it's a valid move that hasn't yet been checked
    if up is valid_move and up not checked:
        liveNodes.insert(board.up())

    if down is valid_move and down not checked:
        liveNodes.insert(board.down())

    if left is valid_move and left not checked:
        liveNodes.insert(board.left())

    if right is valid_move and right not checked:
        liveNodes.insert(board.right())