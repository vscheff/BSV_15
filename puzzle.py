from random import shuffle


solution_sequence = list(range(1, 16)) + [0]

class Puzzle:
    def __init__(self):
        self.grid = [[None for _ in range(4)] for _ in range(4)]
    
    def is_solution(self):
        k = 0
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] != solution_sequence[k]:
                    return False
                k += 1
        return True

    def print_puzzle(self):
        for i in range(4):
            for j in range(4):
                print(f"{self.grid[i][j]:<3}", end='')
            print()

    def randomize(self):
        sequence = list(range(16))
        shuffle(sequence)
        for i in range(4):
            for j in range(4):
                self.grid[i][j] = sequence.pop()


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
                    elif direction == 'down':
                        if i < 3:
                            self.grid[i][j] = self.grid[i+1][j]
                            self.grid[i+1][j] = 0
                    elif direction == 'left':
                        if j > 0:
                            self.grid[i][j] = self.grid[i][j-1]
                            self.grid[i][j-1] = 0
                    elif direction == 'right':
                        if j < 3:
                            self.grid[i][j] = self.grid[i][j+1]
                            self.grid[i][j+1] = 0
                    return


    # chek if a 15 puzzle is solvable or not
    def is_solvable(self, sequence):
        inversions = 0
        for i in range(15):
            for j in range(i+1, 16):
                if sequence[i] > sequence[j]:
                    inversions += 1
        return inversions % 2 == 0
