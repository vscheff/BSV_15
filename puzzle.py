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

