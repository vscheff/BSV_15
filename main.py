from puzzle import *
from minheap import MinHeap
from os import path

TEST_DIR = "test_boards\\"

def main():
    puzzle = get_input_puzzle()

    print(f"\nInput Puzzle (Solvable={puzzle.is_solvable()}):\n{puzzle}")

    if solution := solve_puzzle(puzzle):
        print(f"\nOutput Puzzle:\n{solution}")

def get_input_puzzle():
    while True:
        usr_inp = input("1. Generate a random puzzle\n2. Import a test puzzle\n$ ").strip()
        if usr_inp == '1':
            puzzle = Puzzle()
            puzzle.generate()

            while not puzzle.is_solvable():
                print(f"{puzzle}\nis not solvable. Trying again...")
                puzzle.generate()

            return puzzle

        if usr_inp == '2':
            usr_inp = input("\nEnter filename: ").strip()
            input_board = []

            try:
                with open(f"{TEST_DIR}{usr_inp}", "r") as in_file:
                    for line in in_file:
                        input_board.append([int(n) for n in line.split()])
            except FileNotFoundError:
                print(f"\nERROR: Unable to open {path.dirname(path.realpath(__file__))}\\{TEST_DIR}{usr_inp}\n")
                continue

            return Puzzle(board=input_board)

        print("\nPlease input a valid option!\n")

def solve_puzzle(puzzle: Puzzle):
    live_nodes = MinHeap()
    live_nodes.insert(puzzle)
    current_node = puzzle
    checked_boards = {str(current_node.board): True}

    while live_nodes:
        current_node = live_nodes.pop_root()

        if current_node.is_solution():
            return current_node

        print(f"\nCurrent Node (Cost={current_node.cost}):\n{current_node}")

        for direction in (UP, DOWN, LEFT, RIGHT):
            new_board = current_node.move(direction)
            if new_board and str(new_board) not in checked_boards:
                live_nodes.insert(Puzzle(new_board, current_node.moves + 1))
                checked_boards[str(new_board)] = True
    
    print("No solution found! Are you sure the puzzle was solvable?")


if __name__ == "__main__":
    main()
