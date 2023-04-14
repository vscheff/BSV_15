import matplotlib.pyplot as plt
import pandas as pd

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
    def __init__(self, user: str):
        self.user = user
        self.users = []

        self.dataframes = {INPUT_DF:
                           {"all":  pd.DataFrame(columns=['n', "time"]),
                            "mean": pd.DataFrame(columns=['n', "time"])}}
        for name in POWER_USERS:
            self.dataframes[name] = {"all":  pd.DataFrame(columns=['n', "time"]),
                                     "mean": pd.DataFrame(columns=['n', "time"])}
            self.users.append(name)
        if user not in self.dataframes:
            self.dataframes[user] = {"all":  pd.DataFrame(columns=['n', "time"]),
                                     "mean": pd.DataFrame(columns=['n', "time"])}
            self.users.append(user)

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
        # read all csv files and save them to dataframes
        for user in self.users:
            self.dataframes[user]["all"] = pd.read_csv(f"{DATAFRAME}{user}_all.csv")
            self.dataframes[user]["mean"] = pd.read_csv(f"{DATAFRAME}{user}_mean.csv")

    def plot_all_data(self, debug: bool) -> str:
        figure = plt.figure(figsize=(20, 10))

        keys = iter(colors.keys())
        for user in self.users:
            mean_df = self.dataframes[user]["mean"]
            all_df = self.dataframes[user]["all"]
            plt.plot(mean_df['n'], mean_df["time"], MEAN_SYM, color=colors[next(keys)], label=f"{user}_mean")
            plt.plot(all_df['n'], all_df["time"], ALL_SYM, color=colors[next(keys)], label=f"{user}_all")

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
        mean_df = self.dataframes[INPUT_DF]["mean"]
        plt.plot(mean_df['n'], mean_df["time"], MEAN_SYM, color=colors["blue"], label="Mean time")

        # plot the data for all times as "x" with color2 and label "All times"
        all_df = self.dataframes[INPUT_DF]["all"]
        plt.plot(all_df['n'], all_df["time"], ALL_SYM, color=colors["orange"], label="All times")

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

    # DEBUG - TESTING
    # ------------------------------------------------
    def print_dataframe(self):
        print(f"\n\n\t\tAll times: "
              f"{self.dataframes[INPUT_DF]['all']}"
              f"\n\t\tMean times: "
              f"{self.dataframes[INPUT_DF]['mean']}")
