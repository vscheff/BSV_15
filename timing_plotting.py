import matplotlib.pyplot as plt
import pandas as pd
from os import path
from sys import platform

if platform == "win32":
    DATAFRAME = f"{path.dirname(path.realpath(__file__))}\\dataframes\\"
    PLOTS = f"{path.dirname(path.realpath(__file__))}\\plots\\"
else:
    DATAFRAME = f"{path.dirname(path.realpath(__file__))}/dataframes/"
    PLOTS = f"{path.dirname(path.realpath(__file__))}/plots/"


class Plotting:
    def __init__(self, user):
        # colors
        self.color1 = "#2471a3"  # blue
        self.color2 = "#a9cce3"  # light blue
        self.color3 = "#1abc9c"  # green
        self.color4 = "#d0ece7"  # light green
        self.color5 = "#ba4a00"  # orange
        self.color6 = "#edbb99"  # light orange
        self.color7 = "#d4ac0d"  # yellow
        self.color8 = "#f9e79f"  # light yellow
        self.assignment_all = pd.DataFrame(columns=["n", "time"])
        self.assignment_all_mean = pd.DataFrame(columns=["n", "time"])
        self.user = user

    def sort_dataframe(self):
        # sort the dataframe by n
        self.assignment_all = self.assignment_all.sort_values(by=['n'])

    def add_numbers_to_dataframe(self, n, time):
        # add the n and time to the dataframe for all times
        concat = pd.DataFrame({'n': [n], 'time': [time]}, columns=['n', 'time'])
        self.assignment_all = pd.concat([self.assignment_all, concat], ignore_index=True)

    def calculate_mean_time(self):
        # sort the dataframe
        self.sort_dataframe()

        # calculate the mean time for each n
        mean_times = self.assignment_all.groupby('n')['time'].mean().reset_index()

        # add the mean times to the dataframe
        self.assignment_all_mean = pd.concat([self.assignment_all_mean, mean_times], ignore_index=True)

    def dataframe_to_csv(self):
        # save the dataframes to csv files
        self.assignment_all.to_csv(DATAFRAME + self.user + '_all.csv', index=False)
        self.assignment_all_mean.to_csv(DATAFRAME + self.user + '_mean.csv', index=False)

    def plot_data(self, debug):
        # create a new figure
        figure = plt.figure(figsize=(20, 10))

        # plot the data for mean times as a dashed line with color1 and label "Mean time"
        plt.plot(self.assignment_all_mean['n'], self.assignment_all_mean['time'], '--',
                 color=self.color1, label="Mean time")

        # plot the data for all times as "x" with color2 and label "All times"
        plt.plot(self.assignment_all['n'], self.assignment_all['time'], 'x',
                 color=self.color5, label="All times")

        # add labels and title to the plot
        plt.xlabel("Puzzle size (n)")
        plt.yscale("log")
        plt.ylabel("Time (ns)")
        plt.title("Time to solve the puzzle")

        # add legend
        plt.legend()

        # save the plot
        figure.savefig(PLOTS + self.user + '.png', dpi=300)

        if debug:
            # show the plot
            plt.show()

    # DEBUG - TESTING
    # ------------------------------------------------
    def print_dataframe(self):
        print("\n\n\t\tAll times: ")
        print(self.assignment_all)
        print("\n\t\tMean times: ")
        print(self.assignment_all_mean)
