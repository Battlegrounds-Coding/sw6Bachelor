"THIS IS THE MAIN FILE"
from datetime import timedelta
from python_package.rain import rain_data


def main():
    """main"""

    time = timedelta(seconds=344)

    file = "data\\RainData.csv"

    data = rain_data.save_rain_data(file)

    index = data.get_closest_index(time)

    prediction = data.get_prediction(index)

    print(prediction)


if __name__ == "__main__":
    main()
