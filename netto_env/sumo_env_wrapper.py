import gym
from gym import spaces
import numpy as np
import csv
import os
import traci  # Ensure traci is imported
from sumo_rl import SumoEnvironment
import subprocess

class SumoRLWrapper(gym.Env):
    def __init__(self, **kwargs):
        # Ensure that SUMO starts with sumo.cfg
        sumo_config_file = kwargs.get("sumo_cfg_file", "ABS.sumocfg")  # Default to "ABS.sumocfg"
        self.sumo_process = subprocess.Popen(
            ["sumo-gui", "-c", sumo_config_file] if kwargs["use_gui"] else ["sumo", "-c", sumo_config_file]  # GUI or headless
        )

        # Initialize the SUMO environment
        self.env = SumoEnvironment(
            net_file=kwargs["net_file"],
            route_file=kwargs["route_file"],
            out_csv_name=kwargs["out_csv_name"],
            single_agent=kwargs["single_agent"],
            use_gui=kwargs["use_gui"],
            num_seconds=kwargs["num_seconds"]
        )
        
        obs, _ = self.env.reset()

        # Initialize previous vehicle list
        self.prev_vehicles = set()  # Initialize prev_vehicles as an empty set

        # Define observation and action spaces
        obs_shape = (len(obs),)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=obs_shape, dtype=np.float32)
        self.action_space = spaces.Discrete(self.env.action_space.n)

        # Metrics for analysis
        self.metrics = {
            "avg_speed": [],
            "avg_queue_length": [],
            "teleports": [],
            "collisions": []
        }

        # Global Metrics file for overall tracking
        self.metrics_file = "outputs/metrics.csv"
        self.init_metrics_file()

        # Initialize episode counter
        self.episode_num = 0  # Track episode number

    def init_metrics_file(self):
        os.makedirs(os.path.dirname(self.metrics_file), exist_ok=True)
        if not os.path.exists(self.metrics_file):
            with open(self.metrics_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["episode", "avg_speed", "avg_queue_length", "total_teleports", "total_collisions"])

    def init_episode_file(self, episode_num):
        # Create the episode-specific CSV file dynamically
        self.episode_file = f"outputs/a2c_ABS_conn0_ep{episode_num}.csv"
        os.makedirs(os.path.dirname(self.episode_file), exist_ok=True)  # Ensure directory exists
        if not os.path.exists(self.episode_file):
            with open(self.episode_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["step", "avg_speed", "avg_queue_length", "teleports", "collisions"])

    def reset(self):
        self.episode_num += 1  # Increment episode number
        self.init_episode_file(self.episode_num)  # Initialize episode file
        obs, _ = self.env.reset()
        self.metrics["avg_speed"].clear()
        self.metrics["avg_queue_length"].clear()
        self.metrics["teleports"].clear()
        self.metrics["collisions"].clear()  # Clear collisions for each reset
        self.prev_vehicles = set()  # Reset the previous vehicle list after each reset
        return obs

    def step(self, action):
        obs, reward, done, truncated, info = self.env.step(action)

        # Track current collisions and teleportations
        collisions = self.track_collisions()  # Track collisions using TraCI
        teleports = self.get_teleports()  # Track teleportations (vehicles that left the simulation)
        total_teleports = teleports  # Count the number of teleportations

        # Reward function to penalize for collisions and excessive queue lengths
        reward = self.calculate_reward(collisions, info.get("system_total_stopped", 0))

        # Step-level metric tracking
        self.metrics["avg_speed"].append(info.get("system_mean_speed", 0.0))
        self.metrics["avg_queue_length"].append(info.get("system_total_stopped", 0))  # Fixed typo here
        self.metrics["teleports"].append(total_teleports)
        self.metrics["collisions"].append(collisions)  # Track collisions

        # Append the metrics for each step in CSV
        self.write_step_metrics()

        return obs, reward, done or truncated, info

    def get_teleports(self):
        # Check vehicles that have left the simulation or were teleported
        current_vehicles = set(traci.vehicle.getIDList())  # Get all vehicles currently in the simulation
        departed_vehicles = self.prev_vehicles - current_vehicles  # Vehicles that were removed (departed)
        self.prev_vehicles = current_vehicles  # Update the previous vehicle list
        return len(departed_vehicles)  # Return the count of teleportations

    def track_collisions(self):
        # Track collisions using TraCI's getCollidingVehiclesNumber
        try:
            collision_count = traci.simulation.getCollidingVehiclesNumber()
            return collision_count
        except AttributeError:
            print("Warning: getCollidingVehiclesNumber not available in this SUMO version")
            return 0  # Fallback to 0 if the method is not supported

    def calculate_reward(self, collisions, queue_length):
        # Negative reward for collisions and large queue lengths (penalizing poor performance)
        # Scaled reward function
        collision_penalty = -5 * collisions  # Increased penalty for collisions
        queue_penalty = -0.5 * queue_length  # Adjusted weight for queue length penalty
        return collision_penalty + queue_penalty

    def write_step_metrics(self):
        # Write collisions and other metrics to CSV in real-time
        avg_speed = np.mean(self.metrics["avg_speed"]) if self.metrics["avg_speed"] else 0.0
        avg_queue = np.mean(self.metrics["avg_queue_length"]) if self.metrics["avg_queue_length"] else 0.0
        total_teleports = int(np.sum(self.metrics["teleports"]))
        total_collisions = int(np.sum(self.metrics["collisions"]))  # Sum of collisions

        # Write to the episode-specific CSV file for each step
        with open(self.episode_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([len(self.metrics["avg_speed"]), round(avg_speed, 3), round(avg_queue, 3), total_teleports, total_collisions])

    def write_episode_metrics(self, episode_num):
        avg_speed = np.mean(self.metrics["avg_speed"]) if self.metrics["avg_speed"] else 0.0
        avg_queue = np.mean(self.metrics["avg_queue_length"]) if self.metrics["avg_queue_length"] else 0.0
        total_teleports = int(np.sum(self.metrics["teleports"]))
        total_collisions = int(np.sum(self.metrics["collisions"]))  # Sum of collisions

        # Write to the global CSV file after each episode
        with open(self.metrics_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([episode_num, round(avg_speed, 3), round(avg_queue, 3), total_teleports, total_collisions])

    def render(self, mode="human"):
        pass

    def close(self):
        self.env.close()
        # Ensure to stop the SUMO process after training
        self.sumo_process.terminate()












