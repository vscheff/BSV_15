from os import getcwd
from sys import platform
from typing import TextIO

if platform == "win32":
    TEST_DIR = f"{getcwd()}\\test_boards\\"
else:
    TEST_DIR = f"{getcwd()}/test_boards/"

def get_int_from_user(prompt: str, min_val: int = None, max_val: int = None) -> int:
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

def get_board_from_file() -> list:
    while True:
        with open_board_file() as in_file:
            try:
                return [[int(i) for i in line.split()] for line in in_file]
            except ValueError:
                print("\nERROR: Selected input file is not formatted correctly.")
                continue

def open_board_file() -> TextIO:
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
