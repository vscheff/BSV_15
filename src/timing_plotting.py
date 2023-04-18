import matplotlib.pyplot as plt
import pandas as pd
from random import seed
from time import perf_counter_ns
from tqdm import tqdm

# Local Dependencies
from src.input_handler import get_int_from_user
from src.puzzle import Puzzle, solve_puzzle

# Constant file paths
DATAFRAMES = "./dataframes/"
PLOTS = "./plots/"

# Usernames for users who's data is expected to be present in repo
POWER_USERS = ("bdub", "sam", "von")

# Chart constants
MEAN_SYM = "--"
ALL_SYM = 'x'
X_AXIS = "Puzzle size [n]"
Y_AXIS = "Time [ns]"
CHART_TITLE = "n-Puzzle Solver Algorithm Analysis\n" \
              "Grid Size vs Time Required"
CHART_SIZE = (20, 10)
CHART_DPI = 300

# Color mapping
colors = {
    "blue":         "#2471a3",
    "light_blue":   "#a9cce3",
    "yellow":       "#d4ac0d",
    "light_yellow": "#f9e79f",
    "orange":       "#ba4a00",
    "light_orange": "#edbb99",
    "grey":         "#283747",
    "light_grey":   "#85929E"
}


# Holds all attributes and methods necessary to gather and plot experimental timing data
# attr       user - username of the user executing the program
# attr      users - list of power users and current user
# attr dataframes - dictionary of dataframes for each user
class Plotting:
    def __init__(self):
        # Force user to enter a non-empty string for their username
        self.user = ""
        while not self.user:
            self.user = input("\nEnter your username: ").lower()

        self.users = [i for i in POWER_USERS]

        # Add dataframes for new data, for each power user, and for the current user
        self.dataframes = {name:
                           {"all":  pd.DataFrame(columns=['n', "time"]),
                            "mean": pd.DataFrame(columns=['n', "time"])}
                           for name in POWER_USERS
                           }
        if self.user not in self.dataframes:
            self.dataframes[self.user] = {"all":  pd.DataFrame(columns=['n', "time"]),
                                          "mean": pd.DataFrame(columns=['n', "time"])}
            self.users.append(self.user)

    # Add the timing data of an individual run to the input dataframe
    def add_numbers_to_dataframe(self, n: int, time: int):
        self.dataframes[self.user]["all"].loc[-1] = [n, time]
        self.dataframes[self.user]["all"].index += 1

    # Reads in dataframes for all users from .csv files in the dataframes directory
    def read_csv(self):
        users_not_found = []

        # Read all csv files and save them to dataframes, skipping any users not found
        for user in self.users:
            try:
                self.dataframes[user]["all"] = pd.read_csv(f"{DATAFRAMES}{user}_all.csv")
                self.dataframes[user]["mean"] = pd.read_csv(f"{DATAFRAMES}{user}_mean.csv")
            except FileNotFoundError:
                print(f"\nERROR: No experimental data found for {user}.")
                users_not_found.append(user)

        # Remove any users whose data couldn't be imported
        for user in users_not_found:
            self.dataframes.pop(user)
            self.users.remove(user)

    def plot_all_data(self, debug: bool):
        figure = get_figure()

        keys = iter(colors.keys())
        for user in self.users:
            mean_n = self.dataframes[user]["mean"]['n'].to_numpy()
            mean_time = self.dataframes[user]["mean"]["time"].to_numpy()
            all_n = self.dataframes[user]["all"]['n'].to_numpy()
            all_time = self.dataframes[user]["all"]["time"].to_numpy()

            plt.plot(mean_n, mean_time, MEAN_SYM, color=colors[next(keys)], label=f"{user}_mean")
            plt.plot(all_n, all_time, ALL_SYM, color=colors[next(keys)], label=f"{user}_all")

        # add legend
        plt.legend()

        output_file_name = PLOTS + "all" + ".png"
        figure.savefig(output_file_name, dpi=CHART_DPI)
        print(f"\nCombined data plot exported to {output_file_name}")

        if debug:
            plt.show()

    def plot_data(self, debug: bool):
        # create a new figure
        figure = plt.figure(figsize=CHART_SIZE)

        # plot the data for mean times as a dashed line with color1 and label "Mean time"
        mean_n = self.dataframes[self.user]["mean"]['n'].to_numpy()
        mean_time = self.dataframes[self.user]["mean"]["time"].to_numpy()
        plt.plot(mean_n, mean_time, MEAN_SYM, color=colors["blue"], label="Mean time")

        # plot the data for all times as "x" with color2 and label "All times"
        all_n = self.dataframes[self.user]["all"]['n'].to_numpy()
        all_time = self.dataframes[self.user]["all"]["time"].to_numpy()
        plt.plot(all_n, all_time, ALL_SYM, color=colors["orange"], label="All times")

        # add labels and title to the plot
        plt.xlabel(X_AXIS)
        plt.yscale("log")
        plt.ylabel(Y_AXIS)
        plt.title(CHART_TITLE)

        # add legend
        plt.legend()

        # save the plot
        output_file_name = PLOTS + self.user + ".png"
        figure.savefig(output_file_name, dpi=CHART_DPI)
        print(f"\nIndividual data plot exported to {output_file_name}")

        if debug:
            # show the plot
            plt.show()

    def get_experimental_data(self, debug: bool):
        seed(get_int_from_user("Enter a seed: "))
        min_val = get_int_from_user("Enter minimum grid width: ", 1)
        max_val = get_int_from_user("Enter maximum grid width: ", min_val)
        num_tests = get_int_from_user("Enter desired number of tests: ", 1)

        for n in tqdm(range(min_val, max_val + 1), desc="Computing", unit="size", colour="CYAN", mininterval=0):
            puzzle = Puzzle(size=n)
            for _ in tqdm(range(num_tests), desc=f"{n ** 2 - 1:>2} Puzzle", unit="test", colour="CYAN", mininterval=0):
                puzzle.generate()
                start_time = perf_counter_ns()
                solve_puzzle(puzzle)
                self.add_numbers_to_dataframe(n, perf_counter_ns() - start_time)

        # Calculate the mean time for each grid size on the input dataframe
        self.dataframes[self.user]["mean"] = self.dataframes[self.user]["all"].groupby('n')["time"].mean().reset_index()

        # Save the input dataframes to .csv files
        self.dataframes[self.user]["all"].to_csv(DATAFRAMES + self.user + '_all.csv', index=False)
        self.dataframes[self.user]["mean"].to_csv(DATAFRAMES + self.user + '_mean.csv', index=False)

        if debug:
            self.print_dataframe()

    # DEBUG - TESTING
    # ------------------------------------------------
    def print_dataframe(self):
        print(f"\n\n\t\tAll times: "
              f"{self.dataframes[self.user]['all']}"
              f"\n\t\tMean times: "
              f"{self.dataframes[self.user]['mean']}")


def get_figure() -> plt.figure:
    # create a new figure
    figure = plt.figure(figsize=CHART_SIZE)
    plt.xlabel(X_AXIS)
    plt.yscale("log")
    plt.ylabel(Y_AXIS)
    plt.title(CHART_TITLE)
    return figure
