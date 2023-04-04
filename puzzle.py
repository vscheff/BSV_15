from random import shuffle
from copy import deepcopy

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

solution_sequence = list(range(1, 16)) + [0]

class Puzzle:
    def __init__(self, board=None):
        self.board = board if board else [[-1 for _ in range(4)] for _ in range(4)]
        self.cost = self.count_bad_tiles()
        self.blank_pos = ()
        self.inversions = None

    def __str__(self):
        return "\n".join(["".join([f"{str(i):<3}" for i in row]) for row in self.board])

    def __lt__(self, other):
        return self.cost < other.cost if self.cost != other.cost else self.inv_count() < other.inv_count()

    # Checks if the current board is the solution board
    def is_solution(self):
        return self.cost == 0

    # check if a 15 puzzle is solvable or not
    def is_solvable(self):
        inversions = self.inv_count()
        
        if not self.blank_pos:
            self.find_blank_pos()

        x_pos = 4 - self.blank_pos[0]

        if x_pos % 2:
            if not inversions % 2:
                return True
        elif inversions % 2:
            return True
        return False

    def generate(self):
        sequence = list(range(16))
        shuffle(sequence)
        for i in range(4):
            for j in range(4):
                self.board[i][j] = sequence.pop()
       
        self.find_blank_pos()
        self.inv_count()
        self.cost = self.count_bad_tiles()

    def move(self, direction):
        if not self.blank_pos:
            self.find_blank_pos()

        i, j = self.blank_pos

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
            if i < 3:
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
            if j < 3:
                new_board = deepcopy(self.board)
                new_board[i][j] = new_board[i][j + 1]
                new_board[i][j + 1] = 0
                return new_board
        
        return None

    def count_bad_tiles(self):
        count = 0
        k = 0
        for i in range(4):
            for j in range(4):
                if self.board[i][j] and self.board[i][j] != solution_sequence[k]:
                    count += 1
                k += 1
        return count

    # find number of inversions in 15 puzzle
    def inv_count(self):
        if self.inversions is not None:
            return self.inversions

        sequence = []
        for i in range(4):
            for j in range(4):
                sequence.append(self.board[i][j])

        inversions = 0

        for i in range(16):
            for j in range(i, 16):
                if sequence[i] and sequence[j] and sequence[i] > sequence[j]:
                    inversions += 1

        self.inversions = inversions
        return inversions

    # find position of blank tile
    def find_blank_pos(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    self.blank_pos = (i, j)
                    return

