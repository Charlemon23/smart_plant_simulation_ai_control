import numpy as np

class PlantSimulator:
    """
    A realistic, stable, non-explosive CSTR simulation model.
    Temperature and concentration remain bounded for all inputs.
    """

    def __init__(self):
        self.T = 360.0      # Temperature (K)
        self.C = 1.0        # Concentration (mol/L)
        self.dt = 0.1

        # Reaction parameters
        self.k0 = 5e2
        self.Ea = 8000
        self.R = 8.314

        # Cooling & feed coefficients (stronger damping)
        self.cool_coeff = 1500
        self.feed_coeff = 0.3

    def step(self, action):
        coolant = np.clip(action.get("coolant_flow", 0.5), 0, 1)
        feed = np.clip(action.get("feed_rate", 0.5), 0, 1)

        # Reaction rate (bounded)
        rate = self.k0 * np.exp(-self.Ea / (self.R * self.T)) * self.C
        rate = max(0, min(rate, 3.0))  # Hard cap for safety

        # Concentration update
        dC = feed * self.feed_coeff - rate * 0.05
        self.C = max(0.0, min(self.C + dC * self.dt, 2.0))

        # Temperature update
        dT = (rate * 1200) - (coolant * self.cool_coeff)
        self.T = max(300.0, min(self.T + dT * self.dt, 500.0))

        return {
            "T": float(self.T),
            "C": float(self.C),
            "reaction_rate": float(rate)
        }
