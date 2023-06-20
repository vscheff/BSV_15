import matplotlib.pyplot as plt
import pandas as pd
from random import seed
from time import perf_counter_ns
from tqdm import tqdm

# Local Dependencies
from src.input_handler import get_int_from_user
from src.puzzle import Puzzle, solve_puzzle

# Constants
DATAFRAMES = "./dataframes/"            # Directory for importing/exporting .csv files
PLOTS = "./plots/"                      # Directory for exported plots
POWER_USERS = ("bdub", "sam", "von")    # Usernames for users who's data is expected to be present in repo
CHART_SIZE = (20, 10)                   # Dimensions of the exported plots [inches]
CHART_DPI = 300                         # DPI of exported plots
MEAN_SYM = "--"                         # Symbol used for plotting mean times
ALL_SYM = 'x'                           # Symbol used for plotting individual times

# Chart labels
X_AXIS = "Puzzle size [n]"
Y_AXIS = "Time [ns]"
CHART_TITLE = "n-Puzzle Solver Algorithm Analysis\nGrid Size vs Time Required"

# Color mapping (hex color codes)
COLORS = {
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
# attr      debug - enables debug mode when True
# attr       user - username of the user executing the program
# attr      users - list of power users and current user
# attr dataframes - dictionary of dataframes for each user
class Plotting:
    def __init__(self, debug: bool):
        self.debug = debug
        
        # Force user to enter a non-empty string for their username
        self.user = ""
        while not self.user:
            self.user = input("\nEnter your username: ").lower()

        self.users = list(POWER_USERS)
        if self.user not in self.users:
            self.users.append(self.user)

        # Add dataframes for each power user and for the current user
        self.dataframes = {name:
                           {"all":  pd.DataFrame(columns=['n', "time"]),
                            "mean": pd.DataFrame(columns=['n', "time"])}
                           for name in self.users
                           }

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

    # Generates and exports plots for the dataframes
    # param plot_all - indicates whether all data should be plotted, or just the current user's data
    def plot_data(self, plot_all: bool = False):
        figure = plt.figure(figsize=CHART_SIZE)

        if plot_all:
            # Plot the dataframe for each user, iterating through the color dictionary for their plot colors
            colors = iter(COLORS.values())
            for usr in self.users:
                plot_df(self.dataframes[usr], next(colors), f"{usr}_mean", next(colors), f"{usr}_all")
        else:
            plot_df(self.dataframes[self.user], COLORS["blue"], "Mean time", COLORS["orange"], "All times")

        # Configure plot options
        plt.xlabel(X_AXIS)
        plt.yscale("log")
        plt.ylabel(Y_AXIS)
        plt.title(CHART_TITLE)
        plt.legend()

        # Save the plot
        output_file_name = f"{PLOTS}{'all' if plot_all else self.user}.png"
        figure.savefig(output_file_name, dpi=CHART_DPI)
        print(f"\n{'Combined' if plot_all else 'Individual'} data plot exported to {output_file_name}")

        if self.debug:
            plt.show()

    # Gathers timing data for a variable number of grid sizes and test runs
    def get_experimental_data(self):
        seed(input("Enter a seed:\n$ "))
        min_val = get_int_from_user("Enter minimum grid width", 1)
        max_val = get_int_from_user("Enter maximum grid width", min_val)
        num_tests = get_int_from_user("Enter desired number of tests", 1)

        puzzle = Puzzle(size=min_val)

        # Loop for each grid size
        for n in tqdm(range(min_val, max_val + 1), desc="Computing", unit="size", colour="CYAN", mininterval=0):
            # Loop for each test run, storing the timing data to a dataframe
            for _ in tqdm(range(num_tests), desc=f"{n ** 2 - 1:>2} Puzzle", unit="test", colour="CYAN", mininterval=0):
                puzzle.generate(n)

                start_time = perf_counter_ns()
                solve_puzzle(puzzle)
                self.add_numbers_to_dataframe(n, perf_counter_ns() - start_time)

        # Calculate the mean time for each grid size on the input dataframe
        self.dataframes[self.user]["mean"] = self.dataframes[self.user]["all"].groupby('n')["time"].mean().reset_index()

        # Save the input dataframes to .csv files
        self.dataframes[self.user]["all"].to_csv(DATAFRAMES + self.user + '_all.csv', index=False)
        self.dataframes[self.user]["mean"].to_csv(DATAFRAMES + self.user + '_mean.csv', index=False)

        if self.debug:
            print_df(self.dataframes[self.user])


# Prints a dataframe with nice formatting
# param dataframe - dataframe to be printed
def print_df(dataframe: pd.DataFrame):
    print(f"\n\n\t\tAll times: "
          f"{dataframe['all']}"
          f"\n\t\tMean times: "
          f"{dataframe['mean']}")

# Plots a dataframe to the active figure
# param  dataframe - dataframe to be plotted
# param mean_color - color used to plot the mean time
# param mean_label - label to use for the mean time
# param  all_color - color used to plot the individual times
#  aram  all_label - label to use for the individual times
def plot_df(dataframe: pd.DataFrame, mean_color: str, mean_label: str, all_color: str, all_label: str):
    # Plot the data for mean times with MEAN_SYM, mean_color, and mean_label
    mean_n = dataframe["mean"]['n'].to_numpy()
    mean_time = dataframe["mean"]["time"].to_numpy()
    plt.plot(mean_n, mean_time, MEAN_SYM, color=mean_color, label=mean_label)

    # Plot the data for all times with ALL_SYM, all_color, and all_label
    all_n = dataframe["all"]['n'].to_numpy()
    all_time = dataframe["all"]["time"].to_numpy()
    plt.plot(all_n, all_time, ALL_SYM, color=all_color, label=all_label)
