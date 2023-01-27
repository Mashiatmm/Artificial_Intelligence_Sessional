import numpy as np

class player:

    def __init__(self):
        self.bins = [4, 4, 4, 4, 4, 4, 0]

    def total_bins(self):
        return np.sum(self.bins)