from time import perf_counter
from timing_plotting import Plotting

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
    start_solve_puzzle = perf_counter()

    live_nodes = MinHeap()
    live_nodes.insert(puzzle)
    checked_boards = {str(puzzle.board): True}

    while live_nodes:
        current_node = live_nodes.pop_root()

        if current_node.is_solution():
            break

        print(f"\nCurrent Node (Cost={current_node.cost}):\n{current_node}")

        for direction in UP, DOWN, LEFT, RIGHT:
            new_board = current_node.move(direction)
            if new_board and str(new_board) not in checked_boards:
                live_nodes.insert(Puzzle(new_board))
                checked_boards[str(new_board)] = True
    else:
        print("No solution found! Are you sure the puzzle was solvable?")
        return None

    end_solve_puzzle = perf_counter()
    elapsed_time = end_solve_puzzle - start_solve_puzzle
    print("\nTime to solve the puzzle:", elapsed_time, "seconds")

    return current_node
    # TODO:
        # Put into DATAFRAME if we want to time more than one run


if __name__ == "__main__":
    main()
