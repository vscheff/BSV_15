from puzzle import Puzzle


def main():
    puzzle = Puzzle()
    puzzle.randomize()

    while not puzzle.is_solvable():
        print(f"{puzzle}\nis not solvable. Trying again...")
        puzzle.randomize()

    print(f"{puzzle}\nPuzzle is solved: {puzzle.is_solution()}")

    k = 1
    for i in range(4):
        for j in range(4):
            puzzle.grid[i][j] = k
            k += 1
    puzzle.grid[-1][-1] = 0

    print(f"\n{puzzle}\nPuzzle is solved: {puzzle.is_solution()}")


if __name__ == "__main__":
    main()
