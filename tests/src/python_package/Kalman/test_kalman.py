""" def test_filter_case_temperature():
    filter = f.Kalman(np.float64(60), np.float64(100**2), delta=timedelta(seconds=5))
    data = np.array(
        [
            [49.986, 49.986],
            [49.963, 49.974],
            [50.090, 50.016],
            [50.001, 50.012],
            [50.018, 50.013],
            [50.050, 50.020],
            [49.938, 49.978],
            [49.858, 49.985],
            [49.965, 49.982],
            [50.114, 49.999],
        ],
        dtype=np.float64,
    )
    variance = np.float64(0.01)

    for messurement, estimate in data:
        filter.step(TestData(filter.state), TestMeasurementData(messurement, variance))
        a = np.abs(filter.state - estimate, dtype=np.float64)
        print("abs: " + str(a))
        assert a < np.float64(1e-1)
 """
