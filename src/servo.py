class SG90:
    def __init__(self, P, I, D, angle):
        self.MIN_PULSE_WIDTH = 544
        self.MAX_PULSE_WIDTH = 2400

        self.angle = angle

        self.P = P
        self.I = I
        self.D = D

        self.error = 0
        self.prev_error = 0
        self.sum_error = 0

