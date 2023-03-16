from random import shuffle


class Puzzle:
    def __init__(self):
        self.grid = [[None for _ in range(4)] for _ in range(4)]
    
    def is_solution(self):
        solution = list(range(1, 16))
        solution.append(0)
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] != solution.pop(0):
                    return False
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

