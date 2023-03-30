from random import shuffle
from copy import deepcopy


UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

solution_sequence = list(range(1, 16)) + [0]


class Puzzle:
    def __init__(self, board=None, depth=0):
        self.board = board if board else [[-1 for _ in range(4)] for _ in range(4)]
        self.moves = depth
        self.cost = depth + self.count_bad_tiles()
        self.x_pos = None
        self.x_changed = False

    def __str__(self):
        ret_arr = []

        for i in range(4):
            for j in range(4):
                ret_arr.append(f"{self.board[i][j]:<3}")
            ret_arr.append('\n')

        return "".join(ret_arr[:-1])

    def __lt__(self, other):
        return self.cost < other.cost

    # Checks if the current board is the solution board
    def is_solution(self):
        k = 0
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != solution_sequence[k]:
                    return False
                k += 1
        return True

    # check if a 15 puzzle is solvable or not
    def is_solvable(self):
        inversions = self.inv_count()
        x_pos = self.find_x_pos()

        print(f"\nNumber of inversions: {inversions}\n")

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

        self.x_changed = True

    def move(self, direction):
        # find the empty space
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    # move it in the given direction
                    # if the move is not possible, don't do anything
                    # if the move is possible, swap the values
                    if direction == UP:
                        if i > 0:
                            new_board = deepcopy(self.board)
                            new_board[i][j] = new_board[i-1][j]
                            new_board[i-1][j] = 0
                        else:
                            return None
                    elif direction == DOWN:
                        if i < 3:
                            new_board = deepcopy(self.board)
                            self.board[i][j] = self.board[i+1][j]
                            self.board[i+1][j] = 0
                        else:
                            return None
                    elif direction == LEFT:
                        if j > 0:
                            new_board = deepcopy(self.board)
                            new_board[i][j] = new_board[i][j-1]
                            new_board[i][j - 1] = 0
                        else:
                            return None
                    elif direction == RIGHT:
                        if j < 3:
                            new_board = deepcopy(self.board)
                            new_board[i][j] = new_board[i][j+1]
                            new_board[i][j + 1] = 0
                        else:
                            return None

    def count_bad_tiles(self):
        count = 0
        k = 0
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != solution_sequence[k]:
                    count += 1
                k += 1
        return count


    # find number of inversions in 15 puzzle
    def inv_count(self):
        sequence = []
        for i in range(4):
            for j in range(4):
                sequence.append(self.board[i][j])

        inversions = 0

        for i in range(16):
            for j in range(i, 16):
                if sequence[i] and sequence[j] and sequence[i] > sequence[j]:
                    inversions += 1

        return inversions

    # find position of blank tile
    def find_x_pos(self):
        if not self.x_changed:
            return self.x_pos

        self.x_changed = False

        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return 4 - i
