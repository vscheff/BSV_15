from puzzle import *
from minheap import MinHeap

def main():
    puzzle = Puzzle()
    puzzle.generate()

    while not puzzle.is_solvable():
        print(f"{puzzle}\nis not solvable. Trying again...")
        puzzle.generate()

    print(f"{puzzle}\n")

    solution = solve_puzzle(puzzle)

    print(f"{solution}\nPuzzle is solved: {solution.is_solution()}")

    k = 1
    for i in range(4):
        for j in range(4):
            puzzle.board[i][j] = k
            k += 1
    puzzle.board[-1][-1] = 0

    print(f"\n{puzzle}\nPuzzle is solved: {puzzle.is_solution()}")


def solve_puzzle(puzzle: Puzzle):
    live_nodes = MinHeap()
    live_nodes.insert(puzzle)
    current_node = puzzle 
    checked_boards = {str(current_node.board): True}

    while live_nodes.nodes:
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
