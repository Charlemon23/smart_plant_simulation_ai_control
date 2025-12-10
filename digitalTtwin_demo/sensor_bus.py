import numpy as np

class SensorBus:
    def __init__(self, noise_level=0.01):
        self.noise = noise_level

    def read(self, real_values):
        noisy = {}
        for k, v in real_values.items():
            noisy[k] = v + np.random.normal(0, self.noise * v)
        return noisy

