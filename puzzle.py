from random import shuffle


solution_sequence = list(range(1, 16)) + [0]

class Puzzle:
    def __init__(self):
        self.grid = [[None for _ in range(4)] for _ in range(4)]
        self.x_pos = None
        self.x_changed = False
        self.cost = None

    def __str__(self):
        ret_arr = []

        for i in range(4):
            for j in range(4):
                ret_arr.append(f"{self.grid[i][j]:<3}")
            ret_arr.append('\n')

        return "".join(ret_arr[:-1])
    
    def is_solution(self):
        k = 0
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] != solution_sequence[k]:
                    return False
                k += 1
        return True

    def randomize(self):
        sequence = list(range(16))
        shuffle(sequence)
        for i in range(4):
            for j in range(4):
                self.grid[i][j] = sequence.pop()

        self.x_changed = True

    def move(self, direction):
        # find the empty space
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    # move it in the given direction
                    # if the move is not possible, don't do anything
                    # if the move is possible, swap the values
                    if direction == 'up':
                        if i > 0:
                            self.grid[i][j] = self.grid[i-1][j]
                            self.grid[i-1][j] = 0
                            self.x_changed = True
                    elif direction == 'down':
                        if i < 3:
                            self.grid[i][j] = self.grid[i+1][j]
                            self.grid[i+1][j] = 0
                            self.x_changed = True
                    elif direction == 'left':
                        if j > 0:
                            self.grid[i][j] = self.grid[i][j-1]
                            self.grid[i][j - 1] = 0
                            self.x_changed = True
                    elif direction == 'right':
                        if j < 3:
                            self.grid[i][j] = self.grid[i][j+1]
                            self.grid[i][j + 1] = 0
                            self.x_changed = True
                    return

    # find number of inversions in 15 puzzle
    def inv_count(self):
        sequence = []
        for i in range(4):
            for j in range(4):
                sequence.append(self.grid[i][j])

        inversions = 0

        for i in range(16):
            for j in range(i, 16):
                if sequence[i] and sequence[j] and sequence[i] > sequence[j]:
                    inversions += 1

        return inversions

    # find position of x (empty tile)
    def find_x(self):
        if not self.x_changed:
            return self.x_pos

        self.x_changed = False

        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return 4 - i

    # check if a 15 puzzle is solvable or not
    def is_solvable(self):
        inversions = self.inv_count()
        x_pos = self.find_x()

        print(f"\nNumber of inversions: {inversions}\n")

        if x_pos % 2:
            if not inversions % 2:
                return True
        elif inversions % 2:
            return True

        return False




