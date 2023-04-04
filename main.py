# Local dependencies
from puzzle import UP, DOWN, LEFT, RIGHT, Puzzle
from minheap import MinHeap
from input_handler import get_input_puzzle

def main():
    puzzle = get_input_puzzle()

    print(f"\nInput Puzzle (Solvable={puzzle.is_solvable()}):\n{puzzle}")

    if solution := solve_puzzle(puzzle):
        print(f"\nOutput Puzzle:\n{solution}")


def solve_puzzle(puzzle: Puzzle):
    live_nodes = MinHeap()
    live_nodes.insert(puzzle)
    checked_boards = {str(puzzle.board): True}

    while live_nodes:
        current_node = live_nodes.pop_root()

        if current_node.is_solution():
            return current_node

        print(f"\nCurrent Node (Cost={current_node.cost}):\n{current_node}")

        for direction in UP, DOWN, LEFT, RIGHT:
            new_board = current_node.move(direction)
            if new_board and str(new_board) not in checked_boards:
                live_nodes.insert(Puzzle(new_board))
                checked_boards[str(new_board)] = True

    print("No solution found! Are you sure the puzzle was solvable?")


if __name__ == "__main__":
    main()

