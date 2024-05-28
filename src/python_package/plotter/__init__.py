"""Plot data"""

import csv
from typing import Any
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from ..args import ARGS, OutType, OutGraph, out_graph_to_string
from ..out_mode import OutMode


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
    plots.append(axis.plot(coords[0], measured_data_coords, "red", label="Measured height"))
    return plots


def plotting(plot_args: ARGS, water_level_min: int, water_level_max: int, change_array: list[tuple[OutMode, int]]):
    """Function for plotting data"""
    out_type = plot_args.out_type

    font = {
        "family": "serif",
        "color": "black",
        "weight": "normal",
        "size": 9,
    }

    match out_type:
        case OutType.PGF:
            plot_pgf(plot_args, water_level_min, water_level_max, font, change_array)
        case OutType.PNG:
            plot_png(plot_args, water_level_min, water_level_max, font, change_array)
        case _:
            return

    if plot_args.show:
        plt.show()


def plot_png(
    plot_args: ARGS,
    water_level_min: float,
    water_level_max: float,
    font: dict[str, Any],
    change_array: list[tuple[OutMode, int]],
):
    "Plot in png mode"
    i = 1
    _, axis = plt.subplots(2, 2, figsize=(30, 10), gridspec_kw={"height_ratios": [1, 2]})

    axs: dict[OutGraph, tuple[int, Any]] = {
        OutGraph.RAIN: (i, axis[0, 0]),
        OutGraph.CONTROL: (i, axis[0, 1]),
        OutGraph.KALMAN_DELTA: (i, axis[1, 0]),
        OutGraph.KALMAN: (i, axis[1, 1]),
    }

    plt.suptitle(f"{plot_args.name}")

    plot_graphs(plot_args, water_level_min, water_level_max, font, change_array, axs)

    for _, ax in axs.values():
        ax.legend(loc=4)
    if plot_args.out_image is not None:
        plt.savefig(plot_args.out_image, bbox_inches="tight")


def plot_pgf(
    plot_args: ARGS,
    water_level_min: float,
    water_level_max: float,
    font: dict[str, Any],
    change_array: list[tuple[OutMode, int]],
):
    "Plot in pgf mode"
    matplotlib.use("pgf")
    golden_rasio = 2 / (1 + 5**0.5)

    plt.rcParams.update(
        {
            "text.usetex": True,
            "font.family": "sans-serif",
        }
    )

    axs: dict[OutGraph, tuple[int, Any]] = {}
    for i, graph in enumerate(plot_args.out_graph):
        plt.figure(i, figsize=(3.4, 3.4 * golden_rasio))
        axs[graph] = (i, plt.gcf().subplots())

    plot_graphs(plot_args, water_level_min, water_level_max, font, change_array, axs)

    for _, ax in axs.values():
        lines = ax.get_lines()
        plt.setp(lines, linewidth=0.7)

    if plot_args.out_suffix:
        for i, graph in enumerate(plot_args.out_graph):
            file_name = str(plot_args.out_image).split(".")
            suffix = out_graph_to_string(graph)
            file_name.insert(len(file_name) - 1, suffix)
            file_name = ".".join(file_name)
            plt.figure(i)
            plt.tight_layout()
            plt.gcf().savefig(file_name, backend="pgf")
    else:
        plt.tight_layout()
        plt.savefig(plot_args.out_image, backend="pgf")


def plot_graphs(
    plot_args: ARGS,
    water_level_min: float,
    water_level_max: float,
    font: dict[str, Any],
    change_array: list[tuple[OutMode, int]],
    axs: dict[OutGraph, tuple[int, Any]],
):
    "Plots all graphs"
    fontsize = 7
    plt.yticks(font="serif", fontsize="9")

    # TOP LEFT PLOT
    try:
        i, ax = axs[OutGraph.RAIN]
        plt.figure(i)
        plot(plot_args.rain_file, "brown", "Rain", 1, ax)
        ax.set_ylabel("Rain [mm]", fontdict=font)
        ax.set_xlabel("Time [sec]", fontdict=font)
        ax.set_xlim(0, plot_args.time)
    except KeyError:
        pass

    # TOP RIGHT PLOT
    try:
        i, ax = axs[OutGraph.CONTROL]
        plt.figure(i)
        plot(plot_args.data_control, "green", "Control height", 1, ax)
        plot(plot_args.out, "blue", "Estimated height", 1, ax)
        plot(plot_args.data, "red", "Sensor height", 1, ax)
        ax.axhline(water_level_max, linestyle="--", color="lightgray")
        ax.text(700, water_level_max + 50, "Max water", fontsize=fontsize, ha="right", color="lightgray")
        ax.axhline(water_level_min, linestyle="--", color="lightgray")
        ax.text(700, water_level_min + 50, "Min water", fontsize=fontsize, ha="right", color="lightgray")
        ax.set_xlim(0, plot_args.time)
        ax.set_ylabel("Water level [mm]", fontdict=font)
        ax.set_xlabel("Time [sec]", fontdict=font)
    except KeyError:
        pass

    # BOT LEFT PLOT

    color_label_tuples = [
        ("orange", "Main filter"),
        ("magenta", "Constant offset +50"),
        ("black", "Constant offset -50"),
        ("cyan", "15% over"),
        ("purple", "15 % under"),
    ]
    try:
        i, ax = axs[OutGraph.KALMAN_DELTA]
        plt.figure(i)
        plot_kalman_filters_delta(plot_args.kalman, color_label_tuples, 1, ax)
        ax.axhline(0, linestyle="--", color="gray")
        ax.set_ylabel("Water Level [mm] - Messured Level [mm]", fontdict=font)
        ax.set_xlabel("Time [sec]", fontdict=font)
        ax.set_xlim(0, plot_args.time)
    except KeyError:
        pass

    # BOT RIGHT PLOT
    try:
        i, ax = axs[OutGraph.KALMAN]
        plt.figure(i)
        plot_kalman_filters_state_measured(plot_args.kalman, color_label_tuples, 1, ax)
        plot(plot_args.out, "blue", "Estimated height", 1, ax)
        plot(plot_args.data_control, "green", "Control height", 1, ax)
        ax.set_ylabel("Height [mm]", fontdict=font)
        ax.set_xlabel("Time [sec]", fontdict=font)
        ax.set_xlim(0, plot_args.time)
    except KeyError:
        pass

    plot_change_lines(font, change_array, axs)


def plot_change_lines(
    font: dict[str, Any],
    change_array: list[tuple[OutMode, int]],
    axs: dict[OutGraph, tuple[int, Any]],
):
    "Plots the change list to all plots but RAIN"
    # PRINT CHANGE ARRAYS
    font["size"] = 7

    for mode, pos in change_array:
        text = {OutMode.SENSOR: "Sensor", OutMode.VIRTUAL: "Virtual", OutMode.SENSOR_ERROR: "Sensor Error"}[mode]

        for key, (i, ax) in axs.items():
            if key is OutGraph.RAIN:
                continue
            plt.figure(i)
            ymin, ymax = ax.get_ylim()
            ax.axvline(pos, linestyle="--", color="gray")
            ax.text(
                pos + 50,
                ymin + (ymax - ymin) * 0.02,
                text,
                fontdict=font,
                ha="left",
                va="bottom",
                rotation=90,
                color="gray",
            )

    for i, ax in axs.values():
        plt.figure(i)
        ax.xaxis.set_minor_locator(MultipleLocator(1000))
