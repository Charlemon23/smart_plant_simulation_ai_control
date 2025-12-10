import numpy as np

class SensorBus:
    def __init__(self, noise_level=0.01):
        self.noise = noise_level

    def read(self, real_values):
        noisy = {}
        for k, v in real_values.items():
            # Ensure noise scale is ALWAYS positive and nonzero
            scale = max(1e-6, abs(self.noise * v))
            noise = np.random.normal(0, scale)

            noisy[k] = v + noise
        return noisy
