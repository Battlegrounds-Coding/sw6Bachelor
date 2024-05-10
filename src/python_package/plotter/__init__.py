"""Plot data"""

import csv
import os
from ..args import ARGS
from matplotlib import pyplot as plt


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


def plotting(plot_args: ARGS):
    """Function for plotting data"""

    directory = "experiment_data_results"
    if not os.path.exists(directory):
        os.makedirs(directory)

    axs = plt.subplots(2, 1, figsize=(13, 7), gridspec_kw={"height_ratios": [1, 2]})[1]

    plt.suptitle(f"{plot_args.name}")

    plot(plot_args.rain_file, "red", "Rain", 1, axs[0])
    axs[0].set_ylabel("Rain mm")
    axs[0].legend()

    plot(plot_args.out, "blue", "Estimated height", 1, axs[1])
    plot(plot_args.data, "red", "Sensor height", 1, axs[1])
    plot(plot_args.data_control, "green", "Control, fixed orifice", 1, axs[1])
    axs[1].set_ylim(0, 900)
    axs[1].set_ylabel("Water level cm")
    axs[1].set_xlabel("Time sec")
    axs[1].legend()

    if plot_args.out_image is not None:
        print(plot_args.out_image)
        plt.savefig(plot_args.out_image, bbox_inches="tight")
    plt.show()
