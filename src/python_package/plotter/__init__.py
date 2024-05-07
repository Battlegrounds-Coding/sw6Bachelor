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


def find_kalman_cords(file: list, scale: float) -> list:
    """Find coordinates"""
    cords_one = []
    cords_two = []
    cords_three = []
    cords_four = []
    cords_five = []
    cords_six = []
    cords_seven = []
    cords_eight = []
    cords_nine = []
    cords_ten = []
    for i in range(len(file)):
        cords_one.append(file[i][0])
        cords_two.append(file[i][1] * scale)
        cords_three.append(file[i][2])
        cords_four.append(file[i][3] * scale)
        cords_five.append(file[i][4])
        cords_six.append(file[i][5] * scale)
        cords_seven.append(file[i][6])
        cords_eight.append(file[i][7] * scale)
        cords_nine.append(file[i][8])
        cords_ten.append(file[i][9] * scale)

    return [
        cords_one,
        cords_two,
        cords_three,
        cords_four,
        cords_five,
        cords_six,
        cords_seven,
        cords_eight,
        cords_nine,
        cords_ten,
    ]


def plot_kalman_filters(file: str, color_label_tuples: list[tuple[str, str]], scale: float) -> list:
    """ "Plot kalman csv file"""
    data = read_kalman_csv(file)
    cords = find_kalman_cords(data, scale)

    plots = []
    for i, f in enumerate(color_label_tuples):
        plots.append(plt.plot(cords[2 * i], cords[2 * i + 1], f[0], label=f[1]))
    return plots
