from time import perf_counter_ns
from tqdm import tqdm

# Local dependencies
from src.timing_plotting import Plotting
from src.gui import GraphicsEngine
from src.input_handler import get_board_from_file, get_int_from_user
from src.puzzle import Puzzle, solve_puzzle

DEBUG = False


def main():
    prompt_choice = get_int_from_user("1. Launch GUI\n2. Plot Timing Data\n3. Import Test Puzzle", 1, 3)

    if prompt_choice == 1:
        engine = GraphicsEngine(Puzzle(size=get_int_from_user("\nEnter desired grid width: ", 1)))
        engine.launch_gui()

    elif prompt_choice == 2:
        usr = ""
        while not usr:
            usr = input("\nEnter your username: ").lower()

        plots = Plotting(usr)

        if get_int_from_user("\n1. Generate and Plot New Data\n2. Plot existing data", 1, 2) == 2:
            plots.read_csv()
            print(f"\nPlot exported to: {plots.plot_all_data(DEBUG)}")
            return

        min_val = get_int_from_user("\nEnter minimum grid width: ", 1)
        max_val = get_int_from_user("\nEnter maximum grid width: ", min_val)
        num_tests = get_int_from_user("\nEnter desired number of tests: ", 1)

        for n in tqdm(range(min_val, max_val + 1), desc="Computing", unit="size", colour="CYAN", mininterval=0):
            puzzle = Puzzle(size=n)
            for _ in tqdm(range(num_tests), desc=f"{n ** 2 - 1:>2} Puzzle", unit="test", colour="CYAN", mininterval=0):
                puzzle.generate()
                start_time = perf_counter_ns()
                solve_puzzle(puzzle)
                plots.add_numbers_to_dataframe(n, perf_counter_ns() - start_time)

        plots.calculate_mean_time()
        plots.dataframe_to_csv()
        plots.plot_data(DEBUG)

        if DEBUG:
            plots.print_dataframe()

    elif prompt_choice == 3:
        input_board = get_board_from_file()
        puzzle = Puzzle(board=input_board)
        num_tests = get_int_from_user("\nEnter desired number of tests: ", 1)
        total_time = 0

        for _ in range(num_tests):
            start_time = perf_counter_ns()
            solve_puzzle(puzzle)
            total_time += perf_counter_ns() - start_time

            puzzle.set_board(input_board)

        print(f"\nAverage time to solve the puzzle: {total_time // num_tests / 1000000000:.4f} seconds")


if __name__ == "__main__":
    main()
