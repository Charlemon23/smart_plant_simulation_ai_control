import csv
import time
from plant_simulator import PlantSimulator
from sensor_bus import SensorBus
from control_agent import ControlAgent

def run_simulation(timesteps=1000, log_path="run_log.csv"):
    plant = PlantSimulator()
    sensors = SensorBus()
    agent = ControlAgent()

    # Write CSV header
    with open(log_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["step", "T", "C", "coolant_flow", "feed_rate"])

        for step in range(timesteps):
            # Plant physics
            base_state = plant.step({"coolant_flow": 0.5, "feed_rate": 0.5})

            # Sensor reading
            measured = sensors.read(base_state)

            # Controller
            action = agent.get_action(measured)

            # Apply action
            updated = plant.step(action)

            # Log state
            writer.writerow([
                step,
                float(updated["T"]),
                float(updated["C"]),
                float(action["coolant_flow"]),
                float(action["feed_rate"])
            ])

            time.sleep(0.05)

    print("Simulation complete. Data logged to", log_path)

if __name__ == "__main__":
    run_simulation()
