from time import perf_counter_ns
from timing_plotting import Plotting
from tqdm import tqdm

# Local dependencies
from puzzle import UP, DOWN, LEFT, RIGHT, Puzzle
from minheap import MinHeap
from input_handler import get_input_puzzle


def main():
    puzzle, size, num_tests, usr, usr_inp = get_input_puzzle()
    plots = Plotting(usr)

    debug = False
    total_time = 0

    #TODO:
    # 1. Puzzle size should implement by n everytime we call solve_puzzle function in the usr_inp == '3' condition

    if usr_inp == '3':
        for n in tqdm(range(0, size), desc="Solving Puzzles", unit="puzzle", colour="CYAN",
                      bar_format="{l_bar}{bar:20}{r_bar}{bar:-20b}", position=0):
            for _ in tqdm(range(num_tests), desc="Running Tests", unit="test", colour="CYAN",
                          bar_format="{l_bar}{bar:20}{r_bar}{bar:-20b}", position=1, leave=False):
                start_solve_puzzle = perf_counter_ns()
                solve_puzzle(puzzle)
                end_solve_puzzle = perf_counter_ns()

                plots.add_numbers_to_dataframe(n, end_solve_puzzle - start_solve_puzzle)
                total_time += perf_counter_ns() - start_solve_puzzle

        plots.calculate_mean_time()
        plots.dataframe_to_csv()
        plots.plot_data(debug)

        if debug:
            plots.print_dataframe()

    else:
        for n in range(num_tests):
            start_solve_puzzle = perf_counter_ns()
            solution = solve_puzzle(puzzle)

            total_time += perf_counter_ns() - start_solve_puzzle

            print_solution(solution)
            puzzle.generate()

        print(f"Average time to solve the puzzle: {total_time // num_tests / 1000000000:.4f} seconds")


def solve_puzzle(puzzle: Puzzle):
    live_nodes = MinHeap()
    live_nodes.insert(puzzle)
    checked_boards = {str(puzzle.board): True}

    while live_nodes:
        current_node = live_nodes.pop_root()

        if current_node.is_solution():
            return current_node

        for direction in UP, DOWN, LEFT, RIGHT:
            new_board = current_node.move(direction)
            if new_board and str(new_board) not in checked_boards:
                live_nodes.insert(Puzzle(new_board, puzzle.board_size, current_node))
                checked_boards[str(new_board)] = True

    print("\nNo solution found! Are you sure the puzzle was solvable?")
    return None


def print_solution(node: Puzzle):
    path = [node]

    while node.parent:
        node = node.parent
        path.append(node)

    print("\nSolution Path:")
    for i in range(len(path) - 1, -1, -1):
        print(path[i], '\n')


if __name__ == "__main__":
    main()
