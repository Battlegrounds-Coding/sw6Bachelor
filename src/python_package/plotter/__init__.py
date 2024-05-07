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


def plot(file: str, color: str, label: str, scale: float):
    """Plot csv file"""
    data = read_csv(file)
    cords = find_cords(data, scale)

    plots = plt.plot(cords[0], cords[1], color, label=label)

    return plots


def read_kalman_csv(file: str) -> list:
    """Read kalman csv file"""
    data = []
    with open(file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for _, line in enumerate(reader):
            line = str(line[0]).split(",")
            data.append(
                [
                    float(line[0]),
                    float(line[6]),
                    float(line[7]),
                    float(line[13]),
                    float(line[14]),
                    float(line[20]),
                    float(line[21]),
                    float(line[27]),
                    float(line[28]),
                    float(line[34]),
                ]
            )

    return data


def plot_kalman_filters(file: str, color_label_tuples: list[tuple[str, str]], scale: float) -> list:
    """ "Plot kalman csv file"""
    data = read_kalman_csv(file)

    plots = []
    for i, f in enumerate(color_label_tuples):
        plots.append(plt.plot(data[2 * i], data[2 * i + 1] * scale, f[0], f[1]))
    return plots
