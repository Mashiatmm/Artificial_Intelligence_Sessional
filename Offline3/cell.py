class Cell:
    def __init__(self, n, m, k):
        self.edge = 4
        self.corner = 5
        self.prob = 1 / (n*m - k)
        self.obstacle = False
        self.sensed = False
        self.edge_prob = 0.9
        self.corner_prob = 0.1

    def get_edge_prob(self):
        if self.edge == 0:
            self.corner_prob = 1
            return 0
        return self.edge_prob / self.edge

    def get_corner_prob(self):
        return self.corner_prob / self.corner



