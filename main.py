from time import perf_counter_ns

# Local dependencies
from src.gui import GraphicsEngine
from src.input_handler import get_board_from_file, get_int_from_user
from src.puzzle import Puzzle, solve_puzzle
from src.timing_plotting import Plotting

# Enables debug mode when True
DEBUG = False


def main():
    prompt_choice = get_int_from_user("1. Launch GUI\n2. Plot Timing Data\n3. Import Test Puzzle", 1, 3)

    # Launch GUI
    if prompt_choice == 1:
        engine = GraphicsEngine(Puzzle(size=get_int_from_user("Enter desired grid width: ", 1)))
        engine.launch_gui()

    # Plot Timing Data
    elif prompt_choice == 2:
        plots = Plotting()

        # Gather new experimental data if the user requests it
        if get_int_from_user("1. Generate and Plot New Data\n2. Plot existing data", 1, 2) == 1:
            plots.get_experimental_data(DEBUG)

        plots.read_csv()
        plots.plot_data(DEBUG)
        plots.plot_all_data(DEBUG)

    # Import Test Puzzle
    else:
        puzzle = Puzzle(board=get_board_from_file())
        num_tests = get_int_from_user("Enter desired number of tests: ", 1)
        total_time = 0

        # Record time for each individual test run
        for _ in range(num_tests):
            start_time = perf_counter_ns()
            solve_puzzle(puzzle)
            total_time += perf_counter_ns() - start_time

        print(f"\nAverage time to solve the puzzle: {total_time // num_tests / 1000000000:.4f} seconds")


if __name__ == "__main__":
    main()
