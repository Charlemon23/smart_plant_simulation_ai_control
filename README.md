Digital Twin Demonstration Prototype
AI-Controlled Smart Chemical Plant – Simulation & Control Loop Prototype

This module provides a fully functional digital twin prototype integrated into the broader Smart Plant Simulation AI Control system. It is designed for demonstrations, academic presentations, and early-stage research validation before connecting to real simulators such as DWSIM, Factory I/O, or Aspen HYSYS.

1. Overview

The digital twin prototype models a simplified chemical process (CSTR reactor + cooling control loop) and includes:

Virtual plant physics model

Sensor bus (noisy measurements)

AI control agent placeholder (rule-based for demo)

Realtime control loop

System visualization

This mirrors the architecture intended for the full AI-driven autonomous plant.

2. System Architecture
 ┌────────────────┐      ┌──────────────────┐      ┌────────────────────┐
 │ Digital Twin    │ ---> │ Sensor Interface │ ---> │ AI Control Agent    │
 │ (Plant Model)   │      │ (Noisy Readings) │      │ (RL / Rule-Based)   │
 └────────────────┘      └──────────────────┘      └────────────────────┘
          ▲                                                        │
          └────────────────────────────────────────────────────────┘

3. Features

Continuous simulation of temperature and concentration dynamics

Modular components designed to be replaced with real industrial systems

Clean control loop allowing reinforcement learning integration

Visualization for demonstrations

4. Project Structure
digital_twin_demo/
│
├── plant_simulator.py     # Digital plant model (CSTR)
├── sensor_bus.py          # Noisy sensor readings
├── control_agent.py       # Placeholder control agent
├── visualizer.py          # Plots system behavior
├── main.py                # Simulation orchestrator
└── requirements.txt       # Python dependencies

5. Installation
pip install -r requirements.txt

6. Running the Simulation
python main.py


This launches the real-time digital twin demonstration with visualization.

7. Next Steps (Future Integration)

This prototype is designed for seamless expansion to:

Reinforcement learning (PPO, SAC, DQN)

Real-time OPC-UA / MODBUS sensor integration

DWSIM flowsheets for chemical accuracy

Factory I/O or PLC-based control testing

HPC training on LONI (qb3/qb4)
