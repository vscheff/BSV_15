from __future__ import annotations
from random import shuffle
from copy import deepcopy

# Local dependencies
from minheap import MinHeap

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class Puzzle:
    def __init__(self, board: list = None, size: int = 4, parent: Puzzle = None):
        self.parent = parent
        self.cost = -1
        self.blank_pos = (-1, -1)
        self.inversions = -1

        if board is None:
            self.board_size = size
            self.board = [[-1 for _ in range(size)] for _ in range(size)]
            self.generate()
        else:
            self.set_board(board)

    def __str__(self):
        return "\n".join(["".join([f"{str(i):<3}" for i in row]) for row in self.board])

    def __lt__(self, other: Puzzle):
        return self.cost < other.cost if self.cost != other.cost else self.inversions < other.inversions

    def set_board(self, board: list):
        self.board = board
        self.board_size = len(self.board)
        self.cost = self.count_bad_tiles()
        self.blank_pos = self.find_blank_pos()
        self.inversions = self.count_inversions()

    # Checks if the current board is the solution board
    def is_solution(self):
        return self.cost == 0

    # check if a 15 puzzle is solvable or not
    def is_solvable(self):
        x_pos = self.board_size - self.blank_pos[0]

        if self.board_size % 2:
            if not self.inversions % 2:
                return True
        elif x_pos % 2:
            if not self.inversions % 2:
                return True
        elif self.inversions % 2:
            return True
        
        return False

    def is_valid_move(self, move: int):
        i, j = self.blank_pos
        
        return (move == UP and i < self.board_size) or \
               (move == DOWN and i > 0) or \
               (move == LEFT and j < self.board_size) or \
               (move == RIGHT and j > 0) 

    def generate(self):
        sequence = list(range(self.board_size ** 2))
        shuffle(sequence)

        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j] = sequence.pop()

        self.blank_pos = self.find_blank_pos()
        self.inversions = self.count_inversions()
        
        if not self.is_solvable():
            self.generate()
        else:
            self.cost = self.count_bad_tiles()

    def move(self, direction: int):
        i, j = self.blank_pos

        # move it in the given direction
        # if the move is not possible, don't do anything
        # if the move is possible, swap the values
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

    def count_bad_tiles(self):
        count = 0
        k = 1
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] and self.board[i][j] != k:
                    count += 1
                k += 1
        
        return count

    # find number of inversions in 15 puzzle
    def count_inversions(self):
        sequence = []

        for row in self.board:
            sequence.extend(row)

        inversions = 0

        for i in range(self.board_size ** 2):
            for j in range(i + 1, self.board_size ** 2):
                if sequence[i] and sequence[j] and sequence[i] > sequence[j]:
                    inversions += 1

        return inversions

    # find position of blank tile
    def find_blank_pos(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    return i, j


def solve_puzzle(puzzle: Puzzle):
    live_nodes = MinHeap()
    live_nodes.insert(puzzle)
    checked_boards = {str(puzzle.board): True}

    while live_nodes:
        current_node = live_nodes.pop_root()

        if current_node.is_solution():
            return current_node

        for direction in UP, DOWN, LEFT, RIGHT:
            new_board = current_node.move(direction)
            if new_board and str(new_board) not in checked_boards:
                live_nodes.insert(Puzzle(new_board, puzzle.board_size, current_node))
                checked_boards[str(new_board)] = True

    print("\nNo solution found! Are you sure the puzzle was solvable?")
    return None
