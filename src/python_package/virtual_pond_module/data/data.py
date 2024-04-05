class PondData:
    """Data from the virtual pond"""

    def __init__(self, height_over_min, height_overall, overflow):
        self.height_over_min = height_over_min
        self.height_overall = height_overall
        self.overflow = overflow
