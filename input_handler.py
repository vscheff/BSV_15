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
            return Puzzle()

        if usr_inp == '2':
            with open_board_file() as in_file:
                try:
                    input_board = [[int(i) for i in line.split()] for line in in_file]
                except ValueError:
                    print("\nERROR: Selected input file is not formatted correctly.\n")
                    continue

            return Puzzle(board=input_board)

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
