from random import shuffle
from copy import deepcopy

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class Puzzle:
    def __init__(self, board=None, size=4, parent=None):
        self.board_size = size
        self.parent = parent

        if board is None:
            self.board = [[-1 for _ in range(size)] for _ in range(size)]
            self.generate()
        else:
            self.board = board
            self.cost = self.count_bad_tiles()
            self.blank_pos = self.find_blank_pos()
            self.inversions = self.count_inversions()

    def __str__(self):
        return "\n".join(["".join([f"{str(i):<3}" for i in row]) for row in self.board])

    def __lt__(self, other):
        return self.cost < other.cost if self.cost != other.cost else self.inversions < other.inversions

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
        i, j = self.find_blank_pos()

        # move it in the given direction
        # if the move is not possible, don't do anything
        # if the move is possible, swap the values
        if direction == UP:
            if i > 0:
                new_board = deepcopy(self.board)
                new_board[i][j] = new_board[i - 1][j]
                new_board[i - 1][j] = 0
                return new_board
        elif direction == DOWN:
            if i < self.board_size - 1:
                new_board = deepcopy(self.board)
                new_board[i][j] = new_board[i + 1][j]
                new_board[i + 1][j] = 0
                return new_board
        elif direction == LEFT:
            if j > 0:
                new_board = deepcopy(self.board)
                new_board[i][j] = new_board[i][j - 1]
                new_board[i][j - 1] = 0
                return new_board
        elif direction == RIGHT:
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

