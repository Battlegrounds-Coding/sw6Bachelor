"""Plot data"""

import csv
import matplotlib.pyplot as plt


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
    for i in range(len(file)):
        cords_x.append(file[i][0])
        cords_y.append(file[i][1] * scale)

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
    for l in range(len(file)):
        for n, j in enumerate(coord_array):
            if n % 2 == 0:
                j.append(file[l][n])
            else:
                j.append(file[l][n] * scale)

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

    plots = []
    for i, f in enumerate(color_label_tuples):
        plots.append(axis.plot(coords[2 * i], coords[2 * i + 1], f[0], label=f[1]))
    plots.append(
        axis.plot(
            coords[len(color_label_tuples) + 1], coords[len(color_label_tuples) + 2], "orange", label="Measured height"
        )
    )
    return plots
