from __future__ import annotations
from copy import deepcopy
from random import shuffle

# Local Dependencies
from src.minheap import MinHeap

# Used to indicate direction of travel when sliding tiles
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


# Holds all attributes and methods necessary to represent a game board state as a node
# attr     parent - parent node of this board state
# attr       cost - estimated cost of exploring this node
# attr  blank_pos - grid coordinates of the blank tile space
# attr inversions - number of inversions in this board state
# attr board_size - length/width of the game board
# attr      board - 2D array of integers representing the board state
class Puzzle:
    # param  board - 2D array of integers representing the board state
    # param   size - length/width of the game board
    # param parent - parent node of this board state
    def __init__(self, board: list = None, size: int = 4, parent: Puzzle = None):
        self.parent = parent
        self.cost = -1
        self.blank_pos = (-1, -1)
        self.inversions = -1
        self.board_size = -1
        self.board = []

        # Generate a new solvable board if one was not provided, else set the given board
        if board is None:
            self.generate(size)
        else:
            self.set_board(board)

    def __str__(self) -> str:
        return '\n'.join(["".join([f"{str(i):<3}" for i in row]) for row in self.board])

    def __lt__(self, other: Puzzle) -> bool:
        return self.cost < other.cost if self.cost != other.cost else self.inversions < other.inversions

    # Updates the board state of this object and all related attributes
    # param board - 2D array of integers representing the new board state
    def set_board(self, board: list):
        self.board = board
        self.board_size = len(self.board)
        self.cost = self.count_bad_tiles()
        self.blank_pos = self.find_blank_pos()
        self.inversions = self.count_inversions()

    # Checks if the current board is the solution board
    def is_solution(self) -> bool:
        return self.cost == 0

    # Checks if the current board is solvable or not
    def is_solvable(self) -> bool:
        # True when:
        #   n is odd and the number of inversions is even
        #   n is even, blank is on an odd row, and the number of inversions are even
        #   n is even, blank is on even row, and the number of inversions are odd
        if self.board_size % 2:
            if not self.inversions % 2:
                return True
        elif (self.board_size - self.blank_pos[0]) % 2:
            if not self.inversions % 2:
                return True
        elif self.inversions % 2:
            return True
        
        return False

    # Generate a new solvable board state
    def generate(self, new_size: int = None):
        # Resize the board if necessary
        if new_size is not None and new_size != self.board_size:
            self.board_size = new_size
            self.board = [[-1 for _ in range(new_size)] for _ in range(new_size)]

        sequence = list(range(self.board_size ** 2))
        shuffle(sequence)

        # Set each grid position to a random value in range [0, n^2)
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j] = sequence.pop()

        self.blank_pos = self.find_blank_pos()
        self.inversions = self.count_inversions()
        
        if not self.is_solvable():
            self.generate()
        else:
            self.cost = self.count_bad_tiles()

    # Checks if a move is valid for the current board state
    # param move - integer representing the intended direction to move the blank tile
    def is_valid_move(self, move: int) -> bool:
        return (move == UP and self.blank_pos[0] < self.board_size - 1) or \
               (move == DOWN and self.blank_pos[0] > 0) or \
               (move == LEFT and self.blank_pos[1] < self.board_size - 1) or \
               (move == RIGHT and self.blank_pos[1] > 0)

    # Generates a new board by moving the blank tile in the desired direction
    #  param direction - integer representing the direction to move the blank tile
    # return new_board - 2D array of integers representing the board state after moving the blank tile by the direction
    # return      None - if the move was not valid
    def move(self, direction: int) -> list[list[int]] | None:
        i, j = self.blank_pos

        # If the move is valid, deep copy the board and swap the values of the new board. Else, do nothing.
        if direction == DOWN:
            if i > 0:
                new_board = deepcopy(self.board)
                new_board[i][j] = new_board[i - 1][j]
                new_board[i - 1][j] = 0
                return new_board
        elif direction == UP:
            if i < self.board_size - 1:
                new_board = deepcopy(self.board)
                new_board[i][j] = new_board[i + 1][j]
                new_board[i + 1][j] = 0
                return new_board
        elif direction == RIGHT:
            if j > 0:
                new_board = deepcopy(self.board)
                new_board[i][j] = new_board[i][j - 1]
                new_board[i][j - 1] = 0
                return new_board
        elif direction == LEFT:
            if j < self.board_size - 1:
                new_board = deepcopy(self.board)
                new_board[i][j] = new_board[i][j + 1]
                new_board[i][j + 1] = 0
                return new_board

        return None

    # Computes the number of non-blank tiles that are out of place
    # return count - number of non-blank tiles not in their solution spot
    def count_bad_tiles(self) -> int:
        count = 0
        k = 1

        # For each tile in the board, check if it's in the solution spot
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] and self.board[i][j] != k:
                    count += 1
                k += 1
        
        return count

    # Computes the number of inversions on the board
    # return inversions - number of inversions that exist in the current board state
    def count_inversions(self) -> int:
        sequence = sum(self.board, [])
        inversions = 0

        # For each tile on the board, compute how many subsequent tiles are smaller than it
        for i in range(self.board_size ** 2):
            for j in range(i + 1, self.board_size ** 2):
                if sequence[i] and sequence[j] and sequence[i] > sequence[j]:
                    inversions += 1

        return inversions

    # Find position of the blank tile
    # return i, j - grid coordinates of the blank tile on the board
    def find_blank_pos(self) -> tuple[int, int]:
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    return i, j


# Main algorithm for solving a puzzle utilizing the Branch and Bound strategy
#  param       puzzle - Puzzle object holding the initial board state
# return current_node - Puzzle object holding the solution board state
# return         None - if no solution existed for the initial board state
def solve_puzzle(puzzle: Puzzle) -> Puzzle | None:
    live_nodes = MinHeap()
    live_nodes.insert(puzzle)
    checked_boards = {str(puzzle.board): True}

    # Loop so long as there are puzzle nodes in the heap
    while live_nodes:
        current_node = live_nodes.pop_root()

        if current_node.is_solution():
            return current_node

        # For each direction check if the move is valid and not an already checked board
        # Inserts a new Puzzle object into the heap if True
        for direction in UP, DOWN, LEFT, RIGHT:
            new_board = current_node.move(direction)
            if new_board and str(new_board) not in checked_boards:
                live_nodes.insert(Puzzle(new_board, puzzle.board_size, current_node))
                checked_boards[str(new_board)] = True

    print("\nNo solution found! Are you sure the puzzle was solvable?")
    return None
