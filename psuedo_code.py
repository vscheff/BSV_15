class Puzzle:
    def is_solution(self):
        return True if solved else False

    def is_solvable(self):
        return True if possible to solve else False

    def generate(self):
        generate random solvable puzzle

    def move(self, direction):
        move blank spot in direction

    def count_bad_tiles(self):
        return number of nonblank tiles that are out of place

    def inv_count(self):
        return number of inversions

    def find_blank(self):
        return position of blank space

def solve_puzzle(puzzle):
    live_nodes = MinHeap()
    live_nodes.insert(puzzle)
    checked_boards = {puzzle.board: True}

    while not liveNodes.is_empty():
        current_node = live_nodes.pop_root()

        # Try to swap empty space in each direction
        # Add the new board to liveNodes if it's a valid move that hasn't yet been checked
        if up is valid_move and up not checked:
            liveNodes.insert(up)
            checked_boards[up] = True

        if down is valid_move and down not checked:
            liveNodes.insert(down)
            checked_boards[down] = True

        if left is valid_move and left not checked:
            liveNodes.insert(left)
            checked_boards[left] = True

        if right is valid_move and right not checked:
            liveNodes.insert(right)
            checked_boards[right] = True
