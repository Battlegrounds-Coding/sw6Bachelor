"""Get rain data from csv file"""

import csv
from datetime import timedelta
from .artificial_rain import ArtificialVariableRainPrediction


def save_rain_data(file: str) -> ArtificialVariableRainPrediction:
    """Read rain csv in atificial rain"""

    rain_data = ArtificialVariableRainPrediction()

    with open(file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for _, line in enumerate(reader):
            line = str(line[0]).split(",")
            time = timedelta(seconds=float(line[0]))

            rain_data.add_point(time, float(line[1]))

    return rain_data
