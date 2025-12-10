import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self):
        self.T = []
        self.C = []

    def update(self, T, C):
        self.T.append(T)
        self.C.append(C)

    def show(self):
        plt.figure(figsize=(10,5))
        plt.plot(self.T, label="Temperature (K)")
        plt.plot(self.C, label="Concentration (mol/L)")
        plt.legend()
        plt.title("Digital Twin State Over Time")
        plt.xlabel("Timestep")
        plt.grid()
        plt.show()

