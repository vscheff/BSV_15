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
        usr_inp = input("1. Generate a random puzzle\n2. Import a test puzzle\n3. Plotting\n$ ").strip()

        if usr_inp == '1':
            while True:
                try:
                    size = int(input("\nEnter desired grid width: "))
                except ValueError:
                    print("\nERROR: Please enter a valid integer.")
                else:
                    break

            while True:
                try:
                    num_tests = int(input("\nEnter desired number of tests: "))
                except ValueError:
                    print("\nERROR: Please enter a valid integer.")
                else:
                    return Puzzle(size=size), None, num_tests, None, usr_inp

        if usr_inp == '2':
            with open_board_file() as in_file:
                try:
                    input_board = [[int(i) for i in line.split()] for line in in_file]
                except ValueError:
                    print("\nERROR: Selected input file is not formatted correctly.\n")
                    continue
            return Puzzle(board=input_board), None, 1, None, usr_inp

        if usr_inp == '3':
            usr = input("\nEnter your username: ")
            while True:
                try:
                    size = int(input("\nEnter desired grid width: "))
                except ValueError:
                    print("\nERROR: Please enter a valid integer.")
                else:
                    break

            while True:
                try:
                    num_tests = int(input("\nEnter desired number of tests: "))
                except ValueError:
                    print("\nERROR: Please enter a valid integer.")
                else:
                    return Puzzle(size=size), size, num_tests, usr, usr_inp

        print("\nERROR: Please input a valid option.\n")


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
