from plant_simulator import PlantSimulator
from sensor_bus import SensorBus
from control_agent import ControlAgent
from visualizer import Visualizer
import time

def run_simulation(timesteps=200):

    plant = PlantSimulator()
    sensors = SensorBus()
    agent = ControlAgent()
    viz = Visualizer()

    for t in range(timesteps):
        # Real state from plant model
        true_state = plant.step({"coolant_flow": 0.5, "feed_rate": 0.5})

        # Sensor readings fed to AI agent
        sensor_data = sensors.read(true_state)

        # AI agent decides new actions
        action = agent.get_action(sensor_data)

        # Apply control input to plant
        updated_state = plant.step(action)

        viz.update(updated_state["T"], updated_state["C"])

        time.sleep(0.02)  # smooth demo

    viz.show()

if __name__ == "__main__":
    run_simulation()

