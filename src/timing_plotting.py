import matplotlib.pyplot as plt
import pandas as pd
from time import perf_counter_ns
from tqdm import tqdm

# Local Dependencies
from src.input_handler import get_int_from_user
from src.puzzle import Puzzle, solve_puzzle

DATAFRAME = "./dataframes/"
PLOTS = "./plots/"
INPUT_DF = "new_data"

POWER_USERS = ("bdub", "sam", "von")

MEAN_SYM = "--"
ALL_SYM = 'x'
X_AXIS = "Puzzle size [n]"
Y_AXIS = "Time [ns]"
CHART_TITLE = "n-Puzzle Solver Algorithm Analysis\nGrid Size vs Time Required"

# colors
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


class Plotting:
    def __init__(self):
        self.user = ""
        while not self.user:
            self.user = input("\nEnter your username: ").lower()

        self.users = []

        self.dataframes = {INPUT_DF:
                           {"all":  pd.DataFrame(columns=['n', "time"]),
                            "mean": pd.DataFrame(columns=['n', "time"])}}
        for name in POWER_USERS:
            self.dataframes[name] = {"all":  pd.DataFrame(columns=['n', "time"]),
                                     "mean": pd.DataFrame(columns=['n', "time"])}
            self.users.append(name)
        if self.user not in self.dataframes:
            self.dataframes[self.user] = {"all":  pd.DataFrame(columns=['n', "time"]),
                                          "mean": pd.DataFrame(columns=['n', "time"])}
            self.users.append(self.user)

    def sort_dataframe(self):
        # sort the dataframe by n
        self.dataframes[INPUT_DF]["all"].sort_values(by=['n'], inplace=True)

    def add_numbers_to_dataframe(self, n: int, time: int):
        # add the n and time to the dataframe for all times
        concat = pd.DataFrame({'n': [n], 'time': [time]}, columns=['n', 'time'])
        self.dataframes[INPUT_DF]["all"] = pd.concat([self.dataframes[INPUT_DF]["all"], concat], ignore_index=True)

    def calculate_mean_time(self):
        # sort the dataframe
        self.sort_dataframe()

        # calculate the mean time for each n
        mean_df = self.dataframes[INPUT_DF]["all"].groupby('n')["time"].mean().reset_index()

        # add the mean times to the dataframe
        self.dataframes[INPUT_DF]["mean"] = pd.concat([self.dataframes[INPUT_DF]["mean"], mean_df], ignore_index=True)

    def dataframe_to_csv(self):
        # save the dataframes to csv files
        self.dataframes[INPUT_DF]["all"].to_csv(DATAFRAME + self.user + '_all.csv', index=False)
        self.dataframes[INPUT_DF]["mean"].to_csv(DATAFRAME + self.user + '_mean.csv', index=False)

    def read_csv(self):
        users_not_found = []

        # read all csv files and save them to dataframes
        for user in self.users:
            try:
                self.dataframes[user]["all"] = pd.read_csv(f"{DATAFRAME}{user}_all.csv")
                self.dataframes[user]["mean"] = pd.read_csv(f"{DATAFRAME}{user}_mean.csv")
            except FileNotFoundError:
                print(f"\nERROR: No experimental data found for {user}.")
                users_not_found.append(user)

        for user in users_not_found:
            self.dataframes.pop(user)
            self.users.remove(user)

    def plot_all_data(self, debug: bool) -> str:
        figure = plt.figure(figsize=(20, 10))

        keys = iter(colors.keys())
        for user in self.users:
            mean_n = self.dataframes[user]["mean"]['n'].to_numpy()
            mean_time = self.dataframes[user]["mean"]["time"].to_numpy()
            all_n = self.dataframes[user]["all"]['n'].to_numpy()
            all_time = self.dataframes[user]["all"]["time"].to_numpy()

            plt.plot(mean_n, mean_time, MEAN_SYM, color=colors[next(keys)], label=f"{user}_mean")
            plt.plot(all_n, all_time, ALL_SYM, color=colors[next(keys)], label=f"{user}_all")

        plt.xlabel(X_AXIS)
        plt.yscale("log")
        plt.ylabel(Y_AXIS)
        plt.title(CHART_TITLE)
        plt.legend()

        output_file_name = PLOTS + "all" + ".png"
        figure.savefig(output_file_name, dpi=300)

        if debug:
            plt.show()

        return output_file_name

    def plot_data(self, debug: bool):
        # plot all data
        self.read_csv()
        self.plot_all_data(debug)

        # create a new figure
        figure = plt.figure(figsize=(20, 10))

        # plot the data for mean times as a dashed line with color1 and label "Mean time"
        mean_n = self.dataframes[INPUT_DF]["mean"]['n'].to_numpy()
        mean_time = self.dataframes[INPUT_DF]["mean"]["time"].to_numpy()
        plt.plot(mean_n, mean_time, MEAN_SYM, color=colors["blue"], label="Mean time")

        # plot the data for all times as "x" with color2 and label "All times"
        all_n = self.dataframes[INPUT_DF]["all"]['n'].to_numpy()
        all_time = self.dataframes[INPUT_DF]["all"]["time"].to_numpy()
        plt.plot(all_n, all_time, ALL_SYM, color=colors["orange"], label="All times")

        # add labels and title to the plot
        plt.xlabel(X_AXIS)
        plt.yscale("log")
        plt.ylabel(Y_AXIS)
        plt.title(CHART_TITLE)

        # add legend
        plt.legend()

        # save the plot
        figure.savefig(PLOTS + self.user + '.png', dpi=300)

        if debug:
            # show the plot
            plt.show()

    def get_experimental_data(self, debug: bool):
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

        self.calculate_mean_time()
        self.dataframe_to_csv()
        self.plot_data(debug)

        if debug:
            self.print_dataframe()

    # DEBUG - TESTING
    # ------------------------------------------------
    def print_dataframe(self):
        print(f"\n\n\t\tAll times: "
              f"{self.dataframes[INPUT_DF]['all']}"
              f"\n\t\tMean times: "
              f"{self.dataframes[INPUT_DF]['mean']}")
