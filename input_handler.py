from os import path
from sys import platform

# Local dependencies
from puzzle import Puzzle

if platform == "win32":
    TEST_DIR = f"{path.dirname(path.realpath(__file__))}\\test_boards\\"
else:
    TEST_DIR = f"{path.dirname(path.realpath(__file__))}/test_boards/"

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
            input_board = []
            with open_board_file() as in_file:
                for line in in_file:
                    try:
                        input_board.append([int(n) for n in line.split()])
                    except ValueError:
                        break
                else:
                    return Puzzle(board=input_board)

                print("\nERROR: Selected input file is not formatted correctly.\n")
                continue

        print("\nPlease input a valid option!\n")

def open_board_file():
    while True:
        usr_inp = input("\nEnter filename: ").strip()

        try:
            return open(usr_inp)
        except FileNotFoundError:
            pass

        try:
            return open(f"{TEST_DIR}{usr_inp}")
        except FileNotFoundError:
            print(f"\nERROR: Unable to open {TEST_DIR}{usr_inp}")
