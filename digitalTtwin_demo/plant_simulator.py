import numpy as np

class PlantSimulator:
    """
    Simplified digital twin of a continuous stirred tank reactor (CSTR)
    + cooling jacket.

    State variables:
        T = reactor temperature
        C = reactant concentration
    Actions:
        coolant_flow (0–1)
        feed_rate (0–1)
    """

    def __init__(self):
        self.T = 350        # K
        self.C = 1.0        # mol/L
        self.dt = 0.1

    def step(self, action):
        coolant = np.clip(action.get("coolant_flow", 0.5), 0, 1)
        feed = np.clip(action.get("feed_rate", 0.5), 0, 1)

        # Nonlinear dynamics (simplified)
        k0 = 1.2e3
        Ea = 8000
        R = 8.314

        reaction_rate = k0 * np.exp(-Ea / (R * self.T)) * self.C

        dC = feed * 0.5 - reaction_rate * 0.01
        dT = (reaction_rate * 2000) - (coolant * 500)

        # Update state
        self.C += dC * self.dt
        self.T += dT * self.dt

        return {
            "T": self.T,
            "C": self.C,
            "reaction_rate": reaction_rate
        }

