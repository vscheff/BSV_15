import matplotlib.pyplot as plt
import pandas as pd

DATAFRAME = "./dataframes/"
PLOTS = "./plots/"


class Plotting:
    def __init__(self, user):
        # colors
        self.color1 = "#2471a3"  # blue
        self.color2 = "#a9cce3"  # light blue
        self.color3 = "#d4ac0d"  # yellow
        self.color4 = "#f9e79f"  # light yellow
        self.color5 = "#ba4a00"  # orange
        self.color6 = "#edbb99"  # light orange
        self.color7 = "#283747"  # grey
        self.color8 = "#85929E"  # light grey

        self.assignment_all = pd.DataFrame(columns=["n", "time"])
        self.assignment_all_mean = pd.DataFrame(columns=["n", "time"])
        self.dataframe_bdub_all = pd.DataFrame(columns=["n", "time"])
        self.dataframe_bdub_mean = pd.DataFrame(columns=["n", "time"])
        self.dataframe_sam_all = pd.DataFrame(columns=["n", "time"])
        self.dataframe_sam_mean = pd.DataFrame(columns=["n", "time"])
        self.dataframe_von_all = pd.DataFrame(columns=["n", "time"])
        self.dataframe_von_mean = pd.DataFrame(columns=["n", "time"])

        self.dataframe_user_all = pd.DataFrame(columns=["n", "time"])
        self.dataframe_user_mean = pd.DataFrame(columns=["n", "time"])

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

    def read_csv(self):
        # read all csv files and save them to dataframes
        self.dataframe_bdub_all = pd.read_csv(DATAFRAME + 'bdub_all.csv')
        self.dataframe_bdub_mean = pd.read_csv(DATAFRAME + 'bdub_mean.csv')
        self.dataframe_sam_all = pd.read_csv(DATAFRAME + 'sam_all.csv')
        self.dataframe_sam_mean = pd.read_csv(DATAFRAME + 'sam_mean.csv')
        self.dataframe_von_all = pd.read_csv(DATAFRAME + 'von_all.csv')
        self.dataframe_von_mean = pd.read_csv(DATAFRAME + 'von_mean.csv')
        self.dataframe_user_all = pd.read_csv(DATAFRAME + self.user + '_all.csv')
        self.dataframe_user_mean = pd.read_csv(DATAFRAME + self.user + '_mean.csv')

    def plot_all_data(self, debug):
        figure = plt.figure(figsize=(20, 10))
        plt.plot(self.dataframe_bdub_mean['n'], self.dataframe_bdub_mean['time'], '--',
                 color=self.color1, label="bdub_mean")
        plt.plot(self.dataframe_bdub_all['n'], self.dataframe_bdub_all['time'], 'x',
                 color=self.color2, label="bdub_all")
        plt.plot(self.dataframe_sam_mean['n'], self.dataframe_sam_mean['time'], '--',
                 color=self.color3, label="sam_mean")
        plt.plot(self.dataframe_sam_all['n'], self.dataframe_sam_all['time'], 'x', color=self.color4, label="sam_all")
        plt.plot(self.dataframe_von_mean['n'], self.dataframe_von_mean['time'], '--',
                 color=self.color5, label="von_mean")
        plt.plot(self.dataframe_von_all['n'], self.dataframe_von_all['time'], 'x',
                 color=self.color6, label="von_all")
        if self.user != "bdub" and self.user != "sam" and self.user != "von":
            plt.plot(self.dataframe_user_mean['n'], self.dataframe_user_mean['time'], '--',
                     color=self.color7, label=self.user + "_mean")
            plt.plot(self.dataframe_user_all['n'], self.dataframe_user_all['time'], 'x',
                     color=self.color8, label=self.user + "_all")

        plt.xlabel("Puzzle size (n)")
        plt.yscale("log")
        plt.ylabel("Time (ns)")
        plt.title("Time to solve the puzzle")
        plt.legend()

        figure.savefig(PLOTS + 'all' + '.png', dpi=300)

        if debug:
            plt.show()

    def plot_data(self, debug):
        # plot all data
        self.read_csv()
        self.plot_all_data(debug)

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
