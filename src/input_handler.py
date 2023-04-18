from os import getcwd
from sys import platform
from typing import TextIO

if platform == "win32":
    TEST_DIR = f"{getcwd()}\\test_boards\\"
else:
    TEST_DIR = f"{getcwd()}/test_boards/"


# Retrieves a valid integer from the user
#   param prompt - string used to prompt the user for input
#  param min_val - minimum value of the integer
#  param max_val - maximum value of the integer
# return usr_inp - a valid integer within the required range
def get_int_from_user(prompt: str, min_val: int = None, max_val: int = None) -> int:
    # Repeatedly prompt user for input until they input a valid integer within the required range
    while True:
        try:
            usr_inp = int(input(f"\n{prompt}\n$ "))
        except ValueError:
            print("\nERROR: Please enter a valid integer.")
            continue

        if max_val is not None and usr_inp > max_val:
            print(f"Please enter a value less than {max_val + 1}")
        elif min_val is not None and usr_inp < min_val:
            print(f"Please enter a value greater than {min_val - 1}")
        else:
            return usr_inp


# Builds a game board from an input file
# return - 2D array of integers representing the input board state
def get_board_from_file() -> list:
    # Repeatedly prompt the user for input until they input a file containing a properly formatted game board
    while True:
        with open_board_file() as in_file:
            try:
                return [[int(i) for i in line.split()] for line in in_file]
            except ValueError:
                print("\nERROR: Selected input file is not formatted correctly.")
                continue


# Opens an input board file from the test_boards directory
def open_board_file() -> TextIO:
    # Repeatedly prompt the user for input until they input a file that can be opened
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
