from puzzle import Puzzle


def main():
    puzzle = Puzzle()
    puzzle.randomize()
    puzzle.print_puzzle()
    print(f"\nPuzzle is solved: {puzzle.is_solution()}")


if __name__ == "__main__":
    main()
