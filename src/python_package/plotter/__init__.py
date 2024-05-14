"""Plot data"""

import csv
import os
from matplotlib import pyplot as plt
from ..args import ARGS


def read_csv(file: str) -> list:
    """Read csv file"""
    data = []
    with open(file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for _, line in enumerate(reader):
            line = str(line[0]).split(",")
            data.append([float(line[0]), float(line[1])])
    return data


def find_cords(file: list, scale: float) -> list:
    """Find coordinates"""
    cords_x = []
    cords_y = []
    for _, f in enumerate(file):
        cords_x.append(f[0])
        cords_y.append(f[1] * scale)
    return [cords_x, cords_y]


def plot(file: str, color: str, label: str, scale: float, ax):
    """Plot csv file"""
    data = read_csv(file)
    cords = find_cords(data, scale)

    plots = ax.plot(cords[0], cords[1], color, label=label)

    return plots


def read_kalman_csv_delta(file: str, number_of_filters: int) -> list:
    """Read kalman csv file"""
    data = []
    with open(file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for _, line in enumerate(reader):
            line = str(line[0]).split(",")
            temp_list = []  # hack to make data structure work
            i = 0
            while i < number_of_filters:
                temp_list.append(float(line[7 * i]))
                temp_list.append(float(line[7 * i + 6]))
                i += 1
            data.append(temp_list)
    return data


def read_kalman_csv_state_measured(file: str, number_of_filters: int) -> list:
    """Read kalman csv file"""
    data = []
    with open(file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for _, line in enumerate(reader):
            line = str(line[0]).split(",")
            temp_list = []  # hack to make data structure work
            i = 0
            while i < number_of_filters:
                temp_list.append(float(line[7 * i]))
                temp_list.append(float(line[7 * i + 3]))
                i += 1
            temp_list.append(temp_list[0])
            temp_list.append(float(line[7 * i]))
            data.append(temp_list)
    return data


def find_kalman_cords(file: list, scale: float, number_of_filters: int) -> list:
    """Find coordinates"""
    coord_array = []
    i = 0
    while i < number_of_filters:
        coord_array.append([])
        coord_array.append([])
        i += 1
    for _, line in enumerate(file):  # range(len(file)):
        for n, j in enumerate(coord_array):
            if n % 2 == 0:
                j.append(line[n])
            else:
                j.append(line[n] * scale)

    return coord_array


def plot_kalman_filters_delta(file: str, color_label_tuples: list[tuple[str, str]], scale: float, axis) -> list:
    """
    Plot the delta between predicted values and the measured values for each filter.
    This function assumes that the length of color_label_tuples == number of kalman filters
    """
    data = read_kalman_csv_delta(file, len(color_label_tuples))
    coords = find_kalman_cords(data, scale, len(color_label_tuples))

    plots = []
    for i, f in enumerate(color_label_tuples):
        plots.append(axis.plot(coords[2 * i], coords[2 * i + 1], f[0], label=f[1]))
    return plots


def plot_kalman_filters_state_measured(
    file: str, color_label_tuples: list[tuple[str, str]], scale: float, axis
) -> list:
    """
    Plot the measured value and the predicted state for each filter.
    This function assumes that the length of color_label_tuples == number of kalman filters
    """
    data = read_kalman_csv_state_measured(file, len(color_label_tuples))
    coords = find_kalman_cords(data, scale, len(color_label_tuples))

    # Adds the measured data values to a list
    measured_data_coords = []
    with open(file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for _, line in enumerate(reader):
            line = str(line[0]).split(",")
            measured_data_coords.append(float(line[7 * len(color_label_tuples)]))

    plots = []
    for i, f in enumerate(color_label_tuples):
        plots.append(axis.plot(coords[2 * i], coords[2 * i + 1], f[0], label=f[1]))
    plots.append(axis.plot(coords[0], measured_data_coords, "orange", label="Measured height"))
    return plots


def plotting(plot_args: ARGS, out_mode, water_level_min, water_level_max, change_array):
    """Function for plotting data"""
    directory = "experiment_data_results"
    if not os.path.exists(directory):
        os.makedirs(directory)

    _, axs = plt.subplots(2, 2, figsize=(30, 10), gridspec_kw={"height_ratios": [1, 2]})

    fontsize = 7

    plt.suptitle(f"{plot_args.name}")

    for _, i in enumerate(change_array):
        if i[0] == out_mode.SENSOR:
            axs[0, 1].axvline(i[1], linestyle="--", color="gray")
            axs[0, 1].text(
                i[1] + 50, 50, "Mode: Sensor", fontsize=fontsize, ha="left", va="bottom", rotation=90, color="gray"
            )
            axs[1, 1].axvline(i[1], linestyle="--", color="gray")
            axs[1, 1].text(
                i[1] + 50, 50, "Mode: Sensor", fontsize=fontsize, ha="left", va="bottom", rotation=90, color="gray"
            )
            axs[1, 0].axvline(i[1], linestyle="--", color="gray")
            axs[1, 0].text(
                i[1] + 50, 0.5, "Mode: Sensor", fontsize=fontsize, ha="left", va="bottom", rotation=90, color="gray"
            )
        elif i[0] == out_mode.VIRTUAL:
            axs[0, 1].axvline(i[1], linestyle="--", color="gray")
            axs[0, 1].text(
                i[1] + 50, 50, "Mode: Virtual", fontsize=fontsize, ha="left", va="bottom", rotation=90, color="gray"
            )
            axs[1, 1].axvline(i[1], linestyle="--", color="gray")
            axs[1, 1].text(
                i[1] + 50, 50, "Mode: Virtual", fontsize=fontsize, ha="left", va="bottom", rotation=90, color="gray"
            )
            axs[1, 0].axvline(i[1], linestyle="--", color="gray")
            axs[1, 0].text(
                i[1] + 50, 0.5, "Mode: Virtual", fontsize=fontsize, ha="left", va="bottom", rotation=90, color="gray"
            )
        elif i[0] == out_mode.SENSOR_ERROR:
            axs[0, 1].axvline(i[1], linestyle="--", color="gray")
            axs[0, 1].text(
                i[1] + 50, 50, "Sensor error", fontsize=fontsize, ha="left", va="bottom", rotation=90, color="gray"
            )
            axs[1, 1].axvline(i[1], linestyle="--", color="gray")
            axs[1, 1].text(
                i[1] + 50, 50, "Sensor error", fontsize=fontsize, ha="left", va="bottom", rotation=90, color="gray"
            )
            axs[1, 0].axvline(i[1], linestyle="--", color="gray")
            axs[1, 0].text(
                i[1] + 50, 0.5, "Sensor error", fontsize=fontsize, ha="left", va="bottom", rotation=90, color="gray"
            )

    # TOP LEFT PLOT
    plot(plot_args.rain_file, "red", "Rain", 1, axs[0, 0])
    axs[0, 0].set_ylabel("Rain mm")
    axs[0, 0].set_xlabel("Time sec")
    axs[0, 0].set_xlim(0, plot_args.time)
    axs[0, 0].legend(loc=4)

    # TOP RIGHT PLOT
    plot(plot_args.data_control, "green", "Control height", 1, axs[0, 1])
    plot(plot_args.out, "blue", "Estimated height", 1, axs[0, 1])
    plot(plot_args.data, "red", "Sensor height", 1, axs[0, 1])
    axs[0, 1].axhline(water_level_max, linestyle="--", color="lightgray")
    axs[0, 1].text(700, water_level_max + 50, "Max water", fontsize=fontsize, ha="right", color="lightgray")
    axs[0, 1].axhline(water_level_min, linestyle="--", color="lightgray")
    axs[0, 1].text(700, water_level_min + 50, "Min water", fontsize=fontsize, ha="right", color="lightgray")
    axs[0, 1].set_xlim(0, plot_args.time)
    axs[0, 1].set_ylim(0, 1100)
    axs[0, 1].set_ylabel("Water level cm")
    axs[0, 1].set_xlabel("Time sec")
    axs[0, 1].legend(loc=4)

    # BOT LEFT PLOT
    color_label_tuples = [
        ("pink", "Main filter"),
        ("magenta", "Constant offset +50"),
        ("black", "Constant offset -50"),
        ("cyan", "15% over"),
        ("purple", "15 % under"),
    ]
    plot_kalman_filters_delta(plot_args.kalman, color_label_tuples, 1, axs[1, 0])
    axs[1, 0].axhline(0, linestyle="--", color="gray")
    axs[1, 0].set_ylabel("Kalman predicted measured delta")
    axs[1, 0].set_xlabel("Time sec")
    axs[1, 0].set_xlim(0, plot_args.time)
    axs[1, 0].legend(loc=4)

    # BOT RIGHT PLOT
    plot_kalman_filters_state_measured(plot_args.kalman, color_label_tuples, 1, axs[1, 1])
    plot(plot_args.out, "blue", "Estimated height", 1, axs[1, 1])
    plot(plot_args.data, "red", "Sensor height", 1, axs[1, 1])
    plot(plot_args.data_control, "green", "Control height", 1, axs[1, 1])
    axs[1, 1].set_ylabel("Kalman state")
    axs[1, 1].set_xlabel("Time sec")
    axs[1, 1].set_xlim(0, plot_args.time)
    axs[1, 1].set_ylim(0)
    axs[1, 1].legend(loc=4)

    # Save plot as png
    if plot_args.out_image is not None:
        print(plot_args.out_image)
        plt.savefig(plot_args.out_image, bbox_inches="tight")
    plt.show()
