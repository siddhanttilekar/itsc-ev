# Comparative Evaluation of Intelligent Traffic Signal Control for Emergency Vehicle Prioritization

This repository provides a simulation-based evaluation framework comparing different Intelligent Traffic Signal Control (ITSC) strategies for prioritizing emergency vehicles (EVs) operating with blue-light indicators. Built using **SUMO (Simulation of Urban Mobility)** and **TraCI (Traffic Control Interface)**, the simulation models a real-world intersection in Kronach, Germany (near ABS) to evaluate system performance under dynamic traffic conditions.

While the project evaluates multiple control strategies, it specifically highlights the implementation and optimization of **Advantage Actor-Critic (A2C) Deep Reinforcement Learning** for adaptive traffic signal management.

---

## Technical Overview & Intersection Model

The framework models an urban intersection in SUMO based on real-world map data from Kronach, Germany (ABS intersection). Emergency vehicles are introduced with blue-light priority behaviors, including traffic rule overrides and lane-overtaking privileges.

![ABS Intersection SUMO Simulation](Documents/ABS%20Intersection.png)

Three primary signal control strategies are evaluated against an unmanaged baseline:

1. **Baseline (Unmanaged Signal):** Fixed timing without priority logic.
2. **Round Robin (RR):** Fixed-time cyclic phase allocation.
3. **Feedback Control (MONOPOLY):** Rule-based adaptive timing responding to queue lengths and waiting times.
4. **Advantage Actor-Critic (A2C RL):** A deep reinforcement learning agent that dynamically selects signal phases to minimize queue lengths and delays.

---

## A2C Agent Architecture

The Advantage Actor-Critic (A2C) model operates as an actor-critic RL framework:

* **Actor:** Receives state information from the SUMO/TraCI environment and selects signal control actions (green light phase).
* **Critic:** Evaluates the Q-value based on the environment's reward signal and passes the advantage estimate to guide actor updates.

![A2C Architecture](Documents/A2C%20architecture.png)

---

## Key Performance Indicators (KPIs) & Results

Simulations were executed across all control strategies using real-world vehicle flow data collected at the ABS intersection.

![Comparison of the Algorithms with the Baseline](Documents/Comparison%20of%20the%20Algorithms%20with%20the%20Baseline.png)

A comparison of key performance metrics demonstrates the performance advantage of A2C:

| Control Strategy | Average Queue Length (vehicles) | Average Waiting Time (s) | Total Collisions |
| :--- | :--- | :--- | :--- |
| **Round Robin (RR)** | < 120 (accumulative) | < 70.0 | 8 |
| **Feedback Control** | ~6.0 | ~0.2 | 0 |
| **A2C Reinforcement Learning** | **~2.5** | **~0.5** | **0** |

A2C achieved the lowest overall average queue lengths while eliminating intersection collisions entirely during emergency vehicle priority maneuvers.

---

## Conclusion

This study demonstrates the impact of intelligent traffic signal control strategies on emergency vehicle prioritization under blue-light conditions. Static control strategies such as **Round Robin** fail to adapt to unpredictable emergency vehicle arrivals, leading to severe congestion, increased waiting times, and safety hazards.

While **Feedback Control** offers a lightweight and fast rule-based approach, **Advantage Actor-Critic (A2C) Reinforcement Learning** proved to be the most optimal and safest solution. It maintained the lowest queue buildup, reduced overall intersection delays, and completely prevented collisions, making it suitable for deployment in complex urban environments.

---

## Repository Structure

```text
├── assets/                  # Documentation diagrams and plots
│   ├── abs_intersection.png
│   ├── a2c_architecture.png
│   └── algorithm_comparison.png
├── networks/                # SUMO network files (.net.xml, .rou.xml, OSM maps)
├── src/
│   ├── agents/              # A2C Agent, Actor-Critic network models
│   ├── controllers/         # Round Robin & Feedback controller logic
│   └── env/                 # TraCI custom SUMO Gym environments
├── results/                 # Plotting scripts and performance logs
├── main.py                  # Entry point for running simulations/evaluations
├── requirements.txt         # Dependency specifications
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- [SUMO (Simulation of Urban Mobility)](https://eclipse.dev/sumo/) installed and added to environment variables (`SUMO_HOME`).

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/siddhanttilekar/itsc-ev.git
cd itsc-ev
```

2. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

### Running the Simulation

- **Run A2C Agent Evaluation:**

```bash
python main.py --agent a2c --gui
```

- **Run Comparative Baselines:**

```bash
python main.py --agent feedback
python main.py --agent round_robin
```

---

## References & Credits

- Project developed as part of the Scientific Colloquium (System Test & Product Launch) at Hochschule Coburg.
- **Supervised by:** Prof. Dr. Lucila Patiño Studencki
- **Contributors:** Siddhant Anil Tilekar, Nivetha Saravanan, Vaithiyanathan Alagar

